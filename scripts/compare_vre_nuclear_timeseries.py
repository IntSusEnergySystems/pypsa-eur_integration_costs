"""Compare weekly VRE and nuclear generation across overnight scenarios."""

import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import pypsa

logger = logging.getLogger(__name__)

SCENARIOS = [
    "reference",
    "flexible_solar",
    "flexible_onwind",
    "flexible_offshore",
    "flexible_vre",
    "flexible_nuclear",
]
HORIZONS = [2030, 2040, 2050]
VRE_CARRIERS = [
    "solar",
    "solar rooftop",
    "offwind-ac",
    "offwind-dc",
    "onwind",
    "offwind-float",
    "solar-hsat",
]
OUTDIR = Path("results/comparison")


def _generation(n: pypsa.Network, carriers: list[str]) -> pd.Series:
    gens = n.generators.index[n.generators.carrier.isin(carriers)]
    if gens.empty or n.generators_t.p.empty:
        return pd.Series(0.0, index=n.snapshots, name="p")
    cols = [c for c in gens if c in n.generators_t.p.columns]
    if not cols:
        return pd.Series(0.0, index=n.snapshots, name="p")
    return n.generators_t.p[cols].sum(axis=1)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    OUTDIR.mkdir(parents=True, exist_ok=True)
    frames = []
    for scenario in SCENARIOS:
        for year in HORIZONS:
            path = Path(f"results/{scenario}/networks/solved_{year}.nc")
            if not path.exists():
                raise FileNotFoundError(path)
            logger.info("Reading %s", path)
            n = pypsa.Network(path)
            weight = n.snapshot_weightings.generators
            vre = _generation(n, VRE_CARRIERS)
            nuclear = _generation(n, ["nuclear"])
            frames.append(
                pd.DataFrame(
                    {
                        "scenario": scenario,
                        "year": year,
                        "snapshot": vre.index,
                        "vre_mw": vre.to_numpy(),
                        "nuclear_mw": nuclear.reindex(vre.index).fillna(0).to_numpy(),
                        "weight_h": weight.reindex(vre.index).to_numpy(),
                    }
                )
            )
            logger.info(
                "%s %s VRE %.2f TWh, nuclear %.2f TWh",
                scenario,
                year,
                float((vre * weight).sum() / 1e6),
                float((nuclear.reindex(vre.index).fillna(0) * weight).sum() / 1e6),
            )

    df = pd.concat(frames, ignore_index=True)
    csv_path = OUTDIR / "vre_nuclear_generation.csv"
    df.to_csv(csv_path, index=False)
    logger.info("Wrote %s", csv_path)

    fig, axes = plt.subplots(2, 3, figsize=(14, 7), sharex=True, sharey="row")
    for ax, year in zip(axes[0], HORIZONS):
        part = df[df.year == year]
        for scenario, group in part.groupby("scenario"):
            ax.plot(range(len(group)), group.vre_mw.to_numpy(), label=scenario, lw=1)
        ax.set_title(f"VRE {year}")
        ax.set_ylabel("MW")
    for ax, year in zip(axes[1], HORIZONS):
        part = df[df.year == year]
        for scenario, group in part.groupby("scenario"):
            ax.plot(range(len(group)), group.nuclear_mw.to_numpy(), label=scenario, lw=1)
        ax.set_title(f"Nuclear {year}")
        ax.set_ylabel("MW")
        ax.set_xlabel("weekly snapshot")
    axes[0, 0].legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    fig_path = OUTDIR / "vre_nuclear_generation.png"
    fig.savefig(fig_path, dpi=150)
    logger.info("Wrote %s", fig_path)


if __name__ == "__main__":
    main()
