# SPDX-FileCopyrightText: Contributors to PyPSA-Eur <https://github.com/pypsa/pypsa-eur>
#
# SPDX-License-Identifier: MIT

"""Integration-cost constraints that fix flexible-scenario capacities to the reference run."""

import logging

import pandas as pd
import pypsa
import xarray as xr

logger = logging.getLogger(__name__)

VRE_CARRIERS = [
    "solar",
    "solar rooftop",
    "offwind-ac",
    "offwind-dc",
    "onwind",
    "offwind-float",
    "solar-hsat",
]


def _run_name(snakemake) -> str:
    return snakemake.config["run"]["name"]


def _is_flexible_vre(snakemake) -> bool:
    name = _run_name(snakemake)
    return name.startswith("flexible") and name != "flexible_nuclear"


def reference_network(snakemake) -> pypsa.Network:
    horizon = snakemake.wildcards.horizon
    path = f"results/reference/networks/solved_{horizon}.nc"
    logger.info("Loading reference network %s", path)
    return pypsa.Network(path)


def _be_nuclear(n: pypsa.Network) -> pd.Index:
    buses = n.generators.bus
    if "country" in n.buses.columns:
        country = buses.map(n.buses.country)
    else:
        country = buses.astype(str).str[:2]
    return n.generators.index[
        (n.generators.carrier == "nuclear") & (country.astype(str).str[:2] == "BE")
    ]


def fix_be_nuclear(n: pypsa.Network) -> None:
    nuclear = _be_nuclear(n)
    if nuclear.empty:
        logger.warning("No Belgian nuclear generator found; skipping the 2000 MW floor.")
        return
    n.generators.loc[nuclear, "p_nom"] = 2000
    n.generators.loc[nuclear, "p_nom_min"] = 2000


def constraint_vre_capacities(n: pypsa.Network, snakemake) -> pypsa.Network:
    """Freeze VRE or nuclear capacity at the reference optimum before solving."""
    name = _run_name(snakemake)
    foresight = snakemake.params.foresight
    if foresight != "overnight":
        return n

    if _is_flexible_vre(snakemake):
        network = reference_network(snakemake)
        gen_mask = network.generators.carrier.isin(VRE_CARRIERS)
        reference_caps = network.generators.loc[gen_mask, "p_nom_opt"].round(2)
        common = reference_caps.index.intersection(n.generators.index)
        logger.info("Fixing %s VRE generators to the reference optimum.", len(common))
        n.generators.loc[common, "p_nom_min"] = reference_caps.loc[common]
        n.generators.loc[common, "p_nom_max"] = reference_caps.loc[common]
    elif name == "flexible_nuclear":
        network = reference_network(snakemake)
        gen_mask = network.generators.carrier == "nuclear"
        reference_caps = network.generators.loc[gen_mask, "p_nom_opt"].round(2)
        common = reference_caps.index.intersection(n.generators.index)
        logger.info("Fixing %s nuclear generators to the reference optimum.", len(common))
        n.generators.loc[common, "p_nom_min"] = reference_caps.loc[common]
        n.generators.loc[common, "p_nom_max"] = reference_caps.loc[common]
        n.generators.loc[common, "p_nom"] = reference_caps.loc[common]
        n.generators.loc[common, "p_max_pu"] = 0.9999
    return n


def _add_generation_limit(n, network, carriers) -> None:
    def group(df, column="bus"):
        return df[column].to_xarray()

    for carrier in carriers:
        gen_i = n.generators.index[n.generators.carrier == carrier]
        if gen_i.empty:
            logger.info("No generators of type %s found. Skipping.", carrier)
            continue

        local_gen_p = n.model["Generator-p"].loc[:, gen_i].groupby(group(n.generators.loc[gen_i])).sum()
        generation = (local_gen_p * n.snapshot_weightings.generators).sum("snapshot")

        gen_mask = network.generators.carrier == carrier
        dispatch = network.generators_t.p.loc[:, gen_mask]
        weights = network.snapshot_weightings.generators.reindex(dispatch.index)
        data = dispatch.mul(weights, axis=0).sum(axis=0)
        data_xr = data.to_xarray()
        bus_info = network.generators.loc[data_xr.coords["name"].values, "bus"]
        data_xr_bus = data_xr.groupby(xr.DataArray(bus_info, dims="name")).sum()

        for bus in generation.coords["bus"].values:
            if bus not in data_xr_bus.coords["bus"]:
                continue
            n.model.add_constraints(
                generation.sel(bus=bus) <= data_xr_bus.sel(bus=bus),
                name=f"{carrier}_generation_limit_{bus}",
            )
        logger.info("Constraint added for %s.", carrier)


def add_max_vre_constraint(n, snakemake) -> None:
    if not _is_flexible_vre(snakemake):
        return
    if snakemake.params.foresight != "overnight":
        return
    _add_generation_limit(n, reference_network(snakemake), VRE_CARRIERS)


def add_max_nuclear_constraint(n, snakemake) -> None:
    if _run_name(snakemake) != "flexible_nuclear":
        return
    if snakemake.params.foresight != "overnight":
        return
    _add_generation_limit(n, reference_network(snakemake), ["nuclear"])


def add_co2limit_country(n, limit_countries, snakemake, nyears=1.0) -> None:
    """Limit each country's CO2 emissions to a fraction of its 1990 total."""
    from scripts.prepare_sector_network import determine_emission_sectors

    logger.info("Adding a national CO2 budget as a fraction of 1990 levels")
    countries = n.config["countries"]
    sectors = determine_emission_sectors(snakemake.params.sector)

    co2_totals = 1e6 * pd.read_csv(snakemake.input.co2_totals, index_col=0)
    co2_limit_countries = co2_totals.loc[countries, sectors].sum(axis=1)
    co2_limit_countries = co2_limit_countries.loc[
        co2_limit_countries.index.isin(limit_countries.keys())
    ]
    co2_limit_countries *= co2_limit_countries.index.map(limit_countries) * nyears

    p = n.model["Link-p"]
    country = n.links.bus1.map(n.buses.location).map(n.buses.country)
    country_dac = (
        n.links[n.links.carrier == "DAC"].bus3.map(n.buses.location).map(n.buses.country)
    )
    country.loc[country_dac.index] = country_dac

    patterns = [
        "process emissions",
        "HVC to air",
        "electrobiofuels",
        "unsustainable bioliquids",
        "biomass-to-methanol",
        "biomass to liquid",
    ]
    for pattern in patterns:
        source = (
            n.links[n.links.carrier.str.contains(pattern)]
            .bus0.map(n.buses.location)
            .map(n.buses.country)
        )
        country.loc[source.index] = source

    mask = country.isna() | (country == "")
    country.loc[mask] = country.loc[mask].index.str[:2]
    country = country[country != "EU"]

    lhs = []
    for port in [col[3:] for col in n.links if col.startswith("bus")]:
        if port == str(0):
            efficiency = n.links["efficiency"].apply(lambda x: 1.0).rename("efficiency0")
        elif port == str(1):
            efficiency = n.links["efficiency"]
        else:
            efficiency = n.links[f"efficiency{port}"]
        co2_mask = n.links[f"bus{port}"].map(n.buses.carrier).eq("co2")
        idx = n.links[co2_mask].index
        exclude = ["EU oil refining", "EU methanol import", "EU oil import"]
        idx = idx[~pd.Index(idx).isin(exclude)]
        idx = idx[idx.isin(country.index)]
        grouping = country.loc[idx]
        if grouping.isnull().all():
            continue
        expr = (
            (p.loc[:, idx] * efficiency[idx]).groupby(grouping).sum()
            * n.snapshot_weightings.generators
        ).sum("snapshot")
        lhs.append(expr)

    if not lhs:
        logger.warning("No country CO2 terms found; national budget was not added.")
        return

    total = sum(lhs)
    rhs = pd.Series(co2_limit_countries)
    country_dim = list(total.dims)[0]
    for ct in total.indexes[country_dim]:
        n.model.add_constraints(
            total.loc[ct] <= rhs[ct],
            name=f"GlobalConstraint-co2_limit_per_country{ct}",
        )


def add_national_co2_constraints(n, snapshots, snakemake) -> None:
    budgets = snakemake.config.get("co2_budget_national")
    if not budgets:
        return
    nyears = n.snapshot_weightings.generators.sum() / 8760
    investment_year = int(snakemake.wildcards.horizon)
    limit_countries = budgets[investment_year]
    add_co2limit_country(n, limit_countries, snakemake, nyears)
