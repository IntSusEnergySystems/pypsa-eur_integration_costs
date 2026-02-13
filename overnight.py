#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 12:10:59 2025

@author: umair
"""

import pypsa
import pandas as pd
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
current_script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(current_script_dir, "scripts/")
sys.path.append(scripts_path)
from scripts.make_summary import assign_locations
from make_summary import assign_carriers



def rename_techs(label):
    prefix_to_remove = [
        "residential ",
        "services ",
        "urban ",
        "rural ",
        "central ",
        "decentral ",
    ]

    rename_if_contains = [
        # "CHP",
        "gas boiler",
        "biogas",
        "solar thermal",
        "air heat pump",
        "ground heat pump",
        "resistive heater",
        "Fischer-Tropsch",
    ]

    rename_if_contains_dict = {
        "water tanks": "hot water storage",
        "retrofitting": "building retrofitting",
        # "H2 Electrolysis": "hydrogen storage",
        # "H2 Fuel Cell": "hydrogen storage",
        # "H2 pipeline": "hydrogen storage",
        # "battery": "battery storage",
        "H2 for industry": "H2 for industry",
        "land transport fuel cell": "land transport fuel cell",
        "land transport oil": "land transport oil",
        "oil shipping": "shipping oil",
        # "CC": "CC"
    }

    rename = {
        "solar": "solar PV",
        "Sabatier": "methanation",
        "offwind": "offshore wind",
        "offwind-ac": "offshore wind (AC)",
        "offwind-dc": "offshore wind (DC)",
        "onwind": "onshore wind",
        "ror": "hydroelectricity",
        "hydro": "hydroelectricity",
        "PHS": "hydroelectricity",
        "NH3": "ammonia",
        "co2 Store": "DAC",
        "co2 stored": "CO2 sequestration",
        "AC": "transmission lines",
        "DC": "transmission lines",
        "B2B": "transmission lines",
    }

    for ptr in prefix_to_remove:
        if label[: len(ptr)] == ptr:
            label = label[len(ptr) :]

    for rif in rename_if_contains:
        if rif in label:
            label = rif

    for old, new in rename_if_contains_dict.items():
        if old in label:
            label = new

    for old, new in rename.items():
        if old == label:
            label = new
    return label
def rename_techs_tyndp(tech):
    tech = rename_techs(tech)
    if tech in ["H2 Electrolysis", "methanation", 'methanolisation',"helmeth", "H2 liquefaction"]:
        return "power-to-gas"
    elif "H2 pipeline" in tech:
        return "H2 pipeline"
    elif tech in ["nuclear", "uranium"]:
        return "nuclear"
    elif tech in [ "battery charger", "battery discharger"]:
        return "battery storage"
    elif "solar" in tech:
        return "solar"
    elif tech == "Fischer-Tropsch":
        return "power-to-liquid"
    elif "offshore wind" in tech:
        return "offshore wind"
    elif tech in ["CO2 sequestration", "co2", "SMR CC", "process emissions CC","process emissions", "solid biomass for industry CC", "gas for industry CC"]:
         return "CCS"
    elif tech in ["biomass", "biomass boiler", "solid biomass", "solid biomass for industry"]:
         return "biomass"
    elif "load" in tech:
        return "load shedding"
    elif tech == "coal" or tech == "lignite":
          return "coal"
    else:
        return tech
    
#%%

variable_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/reference/networks/base_s_6___2030.nc")
variable_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/reference/networks/base_s_6___2040.nc")
variable_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/reference/networks/base_s_6___2050.nc")

dispatch_solar_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_solar/networks/base_s_6___2030.nc")
dispatch_solar_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_solar/networks/base_s_6___2040.nc")
dispatch_solar_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_solar/networks/base_s_6___2050.nc")

dispatch_onwind_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_onwind/networks/base_s_6___2030.nc")
dispatch_onwind_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_onwind/networks/base_s_6___2040.nc")
dispatch_onwind_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_onwind/networks/base_s_6___2050.nc")

dispatch_offwind_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_offshore/networks/base_s_6___2030.nc")
dispatch_offwind_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_offshore/networks/base_s_6___2040.nc")
dispatch_offwind_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_offshore/networks/base_s_6___2050.nc")

dispatch_vre_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_vre/networks/base_s_6___2030.nc")
dispatch_vre_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_vre/networks/base_s_6___2040.nc")
dispatch_vre_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_vre/networks/base_s_6___2050.nc")

dispatch_nuclear_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_nuclear/networks/base_s_6___2030.nc")
dispatch_nuclear_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_nuclear/networks/base_s_6___2040.nc")
dispatch_nuclear_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/results/flexible_nuclear/networks/base_s_6___2050.nc")

#%%
df_variable=pd.read_csv("/home/umair/pypsa-eur_integration_costs/results/reference/csvs/costs.csv", index_col=2)
df_variable = df_variable.iloc[:, 2:]
df_variable = df_variable.iloc[3:, :]
df_variable = df_variable.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_variable[['2030', '2040', '2050']] = df_variable[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_variable = df_variable.fillna(0)
df_variable.index.name = 'tech'
df_variable = df_variable.groupby('tech').sum().reset_index()
df_variable['tech'] = df_variable['tech'].map(rename_techs_tyndp)
df_variable = df_variable.groupby('tech').sum().reset_index()
df_variable = df_variable.set_index('tech')
costs_variable_2030 = df_variable['2030'].sum()
costs_variable_2040 = df_variable['2040'].sum()
costs_variable_2050 = df_variable['2050'].sum()

df_solar=pd.read_csv("/home/umair/pypsa-eur_integration_costs/results/flexible_solar/csvs/costs.csv", index_col=2)
df_solar = df_solar.iloc[:, 2:]
df_solar = df_solar.iloc[3:, :]
df_solar = df_solar.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_solar[['2030', '2040', '2050']] = df_solar[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_solar = df_solar.fillna(0)
df_solar.index.name = 'tech'
df_solar = df_solar.groupby('tech').sum().reset_index()
df_solar['tech'] = df_solar['tech'].map(rename_techs_tyndp)
df_solar = df_solar.groupby('tech').sum().reset_index()
df_solar = df_solar.set_index('tech')
costs_dispatch_solar_2030 = df_solar['2030'].sum()
costs_dispatch_solar_2040 = df_solar['2040'].sum()
costs_dispatch_solar_2050 = df_solar['2050'].sum()


df_onwind=pd.read_csv("/home/umair/pypsa-eur_integration_costs/results/flexible_onwind/csvs/costs.csv", index_col=2)
df_onwind = df_onwind.iloc[:, 2:]
df_onwind = df_onwind.iloc[3:, :]
df_onwind = df_onwind.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_onwind[['2030', '2040', '2050']] = df_onwind[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_onwind = df_onwind.fillna(0)
df_onwind.index.name = 'tech'
df_onwind = df_onwind.groupby('tech').sum().reset_index()
df_onwind['tech'] = df_onwind['tech'].map(rename_techs_tyndp)
df_onwind = df_onwind.groupby('tech').sum().reset_index()
df_onwind = df_onwind.set_index('tech')
costs_dispatch_onwind_2030 = df_onwind['2030'].sum()
costs_dispatch_onwind_2040 = df_onwind['2040'].sum()
costs_dispatch_onwind_2050 = df_onwind['2050'].sum()

df_offwind=pd.read_csv("/home/umair/pypsa-eur_integration_costs/results/flexible_offshore/csvs/costs.csv", index_col=2)
df_offwind = df_offwind.iloc[:, 2:]
df_offwind = df_offwind.iloc[3:, :]
df_offwind = df_offwind.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_offwind[['2030', '2040', '2050']] = df_offwind[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_offwind = df_offwind.fillna(0)
df_offwind.index.name = 'tech'
df_offwind = df_offwind.groupby('tech').sum().reset_index()
df_offwind['tech'] = df_offwind['tech'].map(rename_techs_tyndp)
df_offwind = df_offwind.groupby('tech').sum().reset_index()
df_offwind = df_offwind.set_index('tech')
costs_dispatch_offwind_2030 = df_offwind['2030'].sum()
costs_dispatch_offwind_2040 = df_offwind['2040'].sum()
costs_dispatch_offwind_2050 = df_offwind['2050'].sum()

df_vre=pd.read_csv("/home/umair/pypsa-eur_integration_costs/results/flexible_vre/csvs/costs.csv", index_col=2)
df_vre = df_vre.iloc[:, 2:]
df_vre = df_vre.iloc[3:, :]
df_vre = df_vre.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_vre[['2030', '2040', '2050']] = df_vre[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_vre = df_vre.fillna(0)
df_vre.index.name = 'tech'
df_vre = df_vre.groupby('tech').sum().reset_index()
df_vre['tech'] = df_vre['tech'].map(rename_techs_tyndp)
df_vre = df_vre.groupby('tech').sum().reset_index()
df_vre = df_vre.set_index('tech')
costs_dispatch_vre_2030 = df_vre['2030'].sum()
costs_dispatch_vre_2040 = df_vre['2040'].sum()
costs_dispatch_vre_2050 = df_vre['2050'].sum()

df_nuclear=pd.read_csv("/home/umair/pypsa-eur_integration_costs/results/flexible_nuclear/csvs/costs.csv", index_col=2)
df_nuclear = df_nuclear.iloc[:, 2:]
df_nuclear = df_nuclear.iloc[3:, :]
df_nuclear = df_nuclear.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_nuclear[['2030', '2040', '2050']] = df_nuclear[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_nuclear = df_nuclear.fillna(0)
df_nuclear.index.name = 'tech'
df_nuclear = df_nuclear.groupby('tech').sum().reset_index()
df_nuclear['tech'] = df_nuclear['tech'].map(rename_techs_tyndp)
df_nuclear = df_nuclear.groupby('tech').sum().reset_index()
df_nuclear = df_nuclear.set_index('tech')
costs_dispatch_nuclear_2030 = df_nuclear['2030'].sum()
costs_dispatch_nuclear_2040 = df_nuclear['2040'].sum()
costs_dispatch_nuclear_2050 = df_nuclear['2050'].sum()

#%%

diff_solar_2030 = (costs_variable_2030 - costs_dispatch_solar_2030)
diff_solar_2040 = (costs_variable_2040 - costs_dispatch_solar_2040)
diff_solar_2050 = (costs_variable_2050 - costs_dispatch_solar_2050)

diff_onwind_2030 = (costs_variable_2030 - costs_dispatch_onwind_2030)
diff_onwind_2040 = (costs_variable_2040 - costs_dispatch_onwind_2040)
diff_onwind_2050 = (costs_variable_2050 - costs_dispatch_onwind_2050)

diff_offwind_2030 = (costs_variable_2030 - costs_dispatch_offwind_2030)
diff_offwind_2040 = (costs_variable_2040 - costs_dispatch_offwind_2040)
diff_offwind_2050 = (costs_variable_2050 - costs_dispatch_offwind_2050)

diff_vre_2030 = (costs_variable_2030 - costs_dispatch_vre_2030)
diff_vre_2040 = (costs_variable_2040 - costs_dispatch_vre_2040)
diff_vre_2050 = (costs_variable_2050 - costs_dispatch_vre_2050)

diff_nuclear_2030 = (costs_variable_2030 - costs_dispatch_nuclear_2030)
diff_nuclear_2040 = (costs_variable_2040 - costs_dispatch_nuclear_2040)
diff_nuclear_2050 = (costs_variable_2050 - costs_dispatch_nuclear_2050)

#%%
technologies_solar = ["solar","solar rooftop","solar-hsat"]
gen_variable_solar_2030 = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies_solar)].sum().sum()
gen_variable_solar_2040 = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies_solar)].sum().sum()
gen_variable_solar_2050 = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies_solar)].sum().sum()
gen_dispatch_solar_2030 = dispatch_solar_2030.generators_t.p.loc[:, dispatch_solar_2030.generators.carrier.isin(technologies_solar)].sum().sum()
gen_dispatch_solar_2040 = dispatch_solar_2040.generators_t.p.loc[:, dispatch_solar_2040.generators.carrier.isin(technologies_solar)].sum().sum()
gen_dispatch_solar_2050 = dispatch_solar_2050.generators_t.p.loc[:, dispatch_solar_2050.generators.carrier.isin(technologies_solar)].sum().sum()

gen_variable_onwind_2030 = variable_2030.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_variable_onwind_2040 = variable_2040.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_variable_onwind_2050 = variable_2050.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_dispatch_onwind_2030 = dispatch_onwind_2030.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_dispatch_onwind_2040 = dispatch_onwind_2040.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_dispatch_onwind_2050 = dispatch_onwind_2050.generators_t.p.filter(like="onwind").sum(axis=1).sum()

technologies_offwind = ["offwind-float", "offwind-ac", "offwind-dc"]
gen_variable_offwind_2030 = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_variable_offwind_2040 = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_variable_offwind_2050 = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_dispatch_offwind_2030 = dispatch_offwind_2030.generators_t.p.loc[:, dispatch_offwind_2030.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_dispatch_offwind_2040 = dispatch_offwind_2040.generators_t.p.loc[:, dispatch_offwind_2040.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_dispatch_offwind_2050 = dispatch_offwind_2050.generators_t.p.loc[:, dispatch_offwind_2050.generators.carrier.isin(technologies_offwind)].sum().sum()

technologies = ["solar","solar rooftop","solar-hsat", "onwind", "offwind-float", "offwind-ac", "offwind-dc"]
gen_variable_vre_2030 = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies)].sum().sum()
gen_variable_vre_2040 = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies)].sum().sum()
gen_variable_vre_2050 = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies)].sum().sum()
gen_dispatch_vre_2030 = dispatch_vre_2030.generators_t.p.loc[:, dispatch_vre_2030.generators.carrier.isin(technologies)].sum().sum()
gen_dispatch_vre_2040 = dispatch_vre_2040.generators_t.p.loc[:, dispatch_vre_2040.generators.carrier.isin(technologies)].sum().sum()
gen_dispatch_vre_2050 = dispatch_vre_2050.generators_t.p.loc[:, dispatch_vre_2050.generators.carrier.isin(technologies)].sum().sum()

gen_variable_nuclear_2030 = variable_2030.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_variable_nuclear_2040 = variable_2040.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_variable_nuclear_2050 = variable_2050.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_dispatch_nuclear_2030 = dispatch_nuclear_2030.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_dispatch_nuclear_2040 = dispatch_nuclear_2040.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_dispatch_nuclear_2050 = dispatch_nuclear_2050.generators_t.p.filter(like="nuclear").sum(axis=1).sum()

#%%

inti_solar_2030 = diff_solar_2030 / gen_dispatch_solar_2030
inti_solar_2040 = diff_solar_2040 / gen_dispatch_solar_2040
inti_solar_2050 = diff_solar_2050 / gen_dispatch_solar_2050

inti_onwind_2030 = diff_onwind_2030 / gen_dispatch_onwind_2030
inti_onwind_2040 = diff_onwind_2040 / gen_dispatch_onwind_2040
inti_onwind_2050 = diff_onwind_2050 / gen_dispatch_onwind_2050

inti_offwind_2030 = diff_offwind_2030 / gen_dispatch_offwind_2030
inti_offwind_2040 = diff_offwind_2040 / gen_dispatch_offwind_2040
inti_offwind_2050 = diff_offwind_2050 / gen_dispatch_offwind_2050

inti_vre_2030 = diff_vre_2030 / gen_dispatch_vre_2030
inti_vre_2040 = diff_vre_2040 / gen_dispatch_vre_2040
inti_vre_2050 = diff_vre_2050 / gen_dispatch_vre_2050

inti_nuclear_2030 = diff_nuclear_2030 / gen_dispatch_nuclear_2030
inti_nuclear_2040 = diff_nuclear_2040 / gen_dispatch_nuclear_2040
inti_nuclear_2050 = diff_nuclear_2050 / gen_dispatch_nuclear_2050

#%%

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

# Define years and data
years = ["2030", "2040", "2050"]
technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

# Assign a unique color for each technology
tech_colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}

# Data dictionary (replace with actual values)
inti_data = {
    "solar": [inti_solar_2030, inti_solar_2040, inti_solar_2050],
    "onwind": [inti_onwind_2030, inti_onwind_2040, inti_onwind_2050],
    "offwind": [inti_offwind_2030, inti_offwind_2040, inti_offwind_2050],
    "vre": [inti_vre_2030, inti_vre_2040, inti_vre_2050],
    "nuclear": [inti_nuclear_2030, inti_nuclear_2040, inti_nuclear_2050]
}

# Create subplots: 2 rows (first row with 3 cols, second row with 2 cols)
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Flatten axes for easy iteration
axes = axes.flatten()


# Loop through each technology and create bar plots
for i, tech in enumerate(technologies):
    title_tech = "VRE" if tech.lower() == "vre" else tech.capitalize()
    axes[i].bar(years, inti_data[tech], color=tech_colors[tech],width=0.6)  # Use same color for all years within a tech
    axes[i].set_title(f"{title_tech} Integration Costs", fontsize=15)
    axes[i].set_ylabel("Integration Costs [Eur/MWh]", fontsize=15)
    axes[i].grid(axis="y", linestyle="--", alpha=0.7)
    axes[i].tick_params(axis='x', labelsize=15)  # Adjust x-tick label size
    axes[i].tick_params(axis='y', labelsize=15)
    axes[i].yaxis.set_major_locator(MaxNLocator(integer=True))
    axes[i].set_facecolor('white')
    axes[i].grid(axis="y", linestyle="--", linewidth=0.7, color="gray", alpha=0.7)
    axes[i].set_ylim(0, 60)
# Hide the last empty subplot (only needed if total plots < grid size)
fig.delaxes(axes[-1])

# Adjust layout and show plot
plt.tight_layout()
plt.show()

#%%
scenarios = ["flexible_solar", "flexible_onwind", 
             "flexible_offshore", "flexible_vre", "flexible_nuclear"]

for scenario in scenarios:
    total_generation = pd.read_excel(f"results/{scenario}/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
    total_generation = total_generation.sum(axis=1) * 1e6
    if scenario == "flexible_solar":
        perc_solar_2030 = (gen_dispatch_solar_2030 / total_generation[2030]) * 100
        perc_solar_2040 = (gen_dispatch_solar_2040 / total_generation[2040]) * 100
        perc_solar_2050 = (gen_dispatch_solar_2050 / total_generation[2050]) * 100
    if scenario == "flexible_onwind":
        perc_onwind_2030 = (gen_dispatch_onwind_2030 / total_generation[2030]) * 100
        perc_onwind_2040 = (gen_dispatch_onwind_2040 / total_generation[2040]) * 100
        perc_onwind_2050 = (gen_dispatch_onwind_2050 / total_generation[2050]) * 100
    if scenario == "flexible_offshore":
        perc_offwind_2030 = (gen_dispatch_offwind_2030 / total_generation[2030]) * 100
        perc_offwind_2040 = (gen_dispatch_offwind_2040 / total_generation[2040]) * 100
        perc_offwind_2050 = (gen_dispatch_offwind_2050 / total_generation[2050]) * 100
    if scenario == "flexible_vre":
        perc_vre_2030 = (gen_dispatch_vre_2030 / total_generation[2030]) * 100
        perc_vre_2040 = (gen_dispatch_vre_2040 / total_generation[2040]) * 100
        perc_vre_2050 = (gen_dispatch_vre_2050 / total_generation[2050]) * 100
    if scenario == "flexible_nuclear":
        perc_nuclear_2030 = (gen_dispatch_nuclear_2030 / total_generation[2030]) * 100
        perc_nuclear_2040 = (gen_dispatch_nuclear_2040 / total_generation[2040]) * 100
        perc_nuclear_2050 = (gen_dispatch_nuclear_2050 / total_generation[2050]) * 100

# colors = ["#f9d002", "#235ebc", "#6895dd", "#baf238", "#ff8c00"]

#%%
import matplotlib.ticker as mticker
years = ["2030", "2040", "2050"]
technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]
colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}
markers = ["o", "s", "^"]  # Circle, Square, Triangle for different years

# Store percentage and cost data
percentage_data = {
    "solar": [perc_solar_2030, perc_solar_2040, perc_solar_2050],
    "onwind": [perc_onwind_2030, perc_onwind_2040, perc_onwind_2050],
    "offwind": [perc_offwind_2030, perc_offwind_2040, perc_offwind_2050],
    "vre": [perc_vre_2030, perc_vre_2040, perc_vre_2050],
    "nuclear": [perc_nuclear_2030, perc_nuclear_2040, perc_nuclear_2050],
}

inti_costs_data = {
    "solar": [inti_solar_2030, inti_solar_2040, inti_solar_2050],
    "onwind": [inti_onwind_2030, inti_onwind_2040, inti_onwind_2050],
    "offwind": [inti_offwind_2030, inti_offwind_2040, inti_offwind_2050],
    "vre": [inti_vre_2030, inti_vre_2040, inti_vre_2050],
    "nuclear": [inti_nuclear_2030, inti_nuclear_2040, inti_nuclear_2050],
}

plt.figure(figsize=(10, 6))

# Plot each technology with different markers for each year
for i, year in enumerate(years):
    for tech in technologies:
        plt.plot(
            percentage_data[tech][i],  # X-axis (Percentage)
            inti_costs_data[tech][i],  # Y-axis (Inti Costs)
            marker=markers[i],  # Different marker for each year
            linestyle="-",
            color=colors[tech],
            markersize=12,  # Bigger dots
            label=f"{tech.capitalize()} ({year})" if i == 0 else ""  # Label only once per technology
        )

# Create two separate legends
# 1. Legend for technologies (colors)
tech_legend_elements = [
    plt.Line2D([0], [0], lw=6, color=colors[tech], markersize=12, label=tech.capitalize())
    for tech in technologies
]

# 2. Legend for years (markers)
year_legend_elements = [
    plt.Line2D([0], [0], marker=markers[i], color="w", markerfacecolor="black", markersize=12, label=str(year))
    for i, year in enumerate(years)
]

# Add the first legend (technologies with colors)
tech_legend = plt.legend(handles=tech_legend_elements, bbox_to_anchor=(0.99, 1), fontsize=14,frameon=False)

# Add the second legend (years with markers)
plt.gca().add_artist(tech_legend)  # Add the first legend back after adding the second
year_legend = plt.legend(handles=year_legend_elements,bbox_to_anchor=(0.83, 1), fontsize=14,frameon=False)

# Labels and title
plt.xlabel("Penetration (%)", fontsize=14)
plt.ylabel("Intigration Costs [Eur/MWh]", fontsize=14)

# Increase tick size
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Format x-axis ticks to show percentages
def percentage_format(x, pos):
    return f"{x:.0f}%"

plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(percentage_format))

# Light gray grid for visibility
plt.grid(color="lightgray", linestyle="--", linewidth=0.7, alpha=0.8)

# Set background color to white
plt.gca().set_facecolor("white")

# Adjust layout to fit legends
plt.tight_layout()

# Show the plot
plt.show()

#%%
import matplotlib.ticker as mticker

years = ["PyPSA"]
technologies = ["solar", "wind"]
colors = {
    "solar": "#f9d002",
    "wind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}
markers = ["o", "s", "^"]  # Circle, Square, Triangle for different years

# Store percentage and cost data
percentage_data = {
    "solar": [perc_solar_2050],
    "wind": [perc_onwind_2050],
    # "offwind": [ perc_offwind_2050],
    # "vre": [ perc_vre_2050],
    # "nuclear": [perc_nuclear_2050],
}

inti_costs_data = {
    "solar": [inti_solar_2050],
    "wind": [inti_onwind_2050],
    # "offwind": [ inti_offwind_2050],
    # "vre": [ inti_vre_2050],
    # "nuclear": [inti_nuclear_2050],
}
new_data = {
    "years": ["Ueckerdt", "ScenarioB"],
    "percentage": {
        "solar": [25, 52],
        "wind": [40, 28],
    },
    "cost": {
        "solar": [100, 29],
        "wind": [60, 38],
    }
}

plt.figure(figsize=(10, 6))

for i, year in enumerate(new_data["years"]):
    years.append(year)
    for tech in technologies:
        percentage_data[tech].append(new_data["percentage"][tech][i])
        inti_costs_data[tech].append(new_data["cost"][tech][i])
# Plot each technology with different markers for each year
for i, year in enumerate(years):
    for tech in technologies:
        plt.plot(
            percentage_data[tech][i],  # X-axis (Percentage)
            inti_costs_data[tech][i],  # Y-axis (Inti Costs)
            marker=markers[i],  # Different marker for each year
            linestyle="-",
            color=colors[tech],
            markersize=12,  # Bigger dots
            label=f"{tech.capitalize()} ({year})" if i == 0 else ""  # Label only once per technology
        )

# Create two separate legends
# 1. Legend for technologies (colors)
tech_legend_elements = [
    plt.Line2D([0], [0], lw=6, color=colors[tech], markersize=12, label=tech.capitalize())
    for tech in technologies
]

# 2. Legend for years (markers)
year_legend_elements = [
    plt.Line2D([0], [0], marker=markers[i], color="w", markerfacecolor="black", markersize=12, label=str(year))
    for i, year in enumerate(years)
]

# Add the first legend (technologies with colors)
tech_legend = plt.legend(handles=tech_legend_elements, bbox_to_anchor=(0.99, 1), fontsize=14,frameon=False)

# Add the second legend (years with markers)
plt.gca().add_artist(tech_legend)  # Add the first legend back after adding the second
year_legend = plt.legend(handles=year_legend_elements,bbox_to_anchor=(0.83, 1), fontsize=14,frameon=False)

# Labels and title
plt.xlabel("Penetration (%)", fontsize=14)
plt.ylabel("Intigration Costs [Eur/MWh]", fontsize=14)

# Increase tick size
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

# Format x-axis ticks to show percentages
def percentage_format(x, pos):
    return f"{x:.0f}%"

plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(percentage_format))
plt.xlim(0, 100)
# Light gray grid for visibility
plt.grid(color="lightgray", linestyle="--", linewidth=0.7, alpha=0.8)

# Set background color to white
plt.gca().set_facecolor("white")

# Adjust layout to fit legends
plt.tight_layout()

# Show the plot
plt.show()


#%%
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
technologies_solar = ["solar","solar rooftop","solar-hsat"]
gen_variable_solar_2030_t = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies_solar)].sum(axis=1)/1e3
gen_variable_solar_2040_t = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies_solar)].sum(axis=1)/1e3
gen_variable_solar_2050_t = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies_solar)].sum(axis=1)/1e3
gen_dispatch_solar_2030_t = dispatch_solar_2030.generators_t.p.loc[:, dispatch_solar_2030.generators.carrier.isin(technologies_solar)].sum(axis=1)/1e3
gen_dispatch_solar_2040_t = dispatch_solar_2040.generators_t.p.loc[:, dispatch_solar_2040.generators.carrier.isin(technologies_solar)].sum(axis=1)/1e3
gen_dispatch_solar_2050_t = dispatch_solar_2050.generators_t.p.loc[:, dispatch_solar_2050.generators.carrier.isin(technologies_solar)].sum(axis=1)/1e3

gen_variable_onwind_2030_t = variable_2030.generators_t.p.filter(like="onwind").sum(axis=1)/1e3
gen_variable_onwind_2040_t = variable_2040.generators_t.p.filter(like="onwind").sum(axis=1)/1e3
gen_variable_onwind_2050_t = variable_2050.generators_t.p.filter(like="onwind").sum(axis=1)/1e3
gen_dispatch_onwind_2030_t = dispatch_onwind_2030.generators_t.p.filter(like="onwind").sum(axis=1)/1e3
gen_dispatch_onwind_2040_t = dispatch_onwind_2040.generators_t.p.filter(like="onwind").sum(axis=1)/1e3
gen_dispatch_onwind_2050_t = dispatch_onwind_2050.generators_t.p.filter(like="onwind").sum(axis=1)/1e3

technologies_offwind = ["offwind-float", "offwind-ac", "offwind-dc"]
gen_variable_offwind_2030_t = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies_offwind)].sum(axis=1)/1e3
gen_variable_offwind_2040_t = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies_offwind)].sum(axis=1)/1e3
gen_variable_offwind_2050_t = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies_offwind)].sum(axis=1)/1e3
gen_dispatch_offwind_2030_t = dispatch_offwind_2030.generators_t.p.loc[:, dispatch_offwind_2030.generators.carrier.isin(technologies_offwind)].sum(axis=1)/1e3
gen_dispatch_offwind_2040_t = dispatch_offwind_2040.generators_t.p.loc[:, dispatch_offwind_2040.generators.carrier.isin(technologies_offwind)].sum(axis=1)/1e3
gen_dispatch_offwind_2050_t = dispatch_offwind_2050.generators_t.p.loc[:, dispatch_offwind_2050.generators.carrier.isin(technologies_offwind)].sum(axis=1)/1e3

technologies = ["solar","solar rooftop","solar-hsat", "onwind", "offwind-float", "offwind-ac", "offwind-dc"]
gen_variable_vre_2030_t = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies)].sum(axis=1)/1e3
gen_variable_vre_2040_t = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies)].sum(axis=1)/1e3
gen_variable_vre_2050_t = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies)].sum(axis=1)/1e3
gen_dispatch_vre_2030_t = dispatch_vre_2030.generators_t.p.loc[:, dispatch_vre_2030.generators.carrier.isin(technologies)].sum(axis=1)/1e3
gen_dispatch_vre_2040_t = dispatch_vre_2040.generators_t.p.loc[:, dispatch_vre_2040.generators.carrier.isin(technologies)].sum(axis=1)/1e3
gen_dispatch_vre_2050_t = dispatch_vre_2050.generators_t.p.loc[:, dispatch_vre_2050.generators.carrier.isin(technologies)].sum(axis=1)/1e3

gen_variable_nuclear_2030_t = variable_2030.generators_t.p.filter(like="nuclear").sum(axis=1)/1e3
gen_variable_nuclear_2040_t = variable_2040.generators_t.p.filter(like="nuclear").sum(axis=1)/1e3
gen_variable_nuclear_2050_t = variable_2050.generators_t.p.filter(like="nuclear").sum(axis=1)/1e3
gen_dispatch_nuclear_2030_t = dispatch_nuclear_2030.generators_t.p.filter(like="nuclear").sum(axis=1)/1e3
gen_dispatch_nuclear_2040_t = dispatch_nuclear_2040.generators_t.p.filter(like="nuclear").sum(axis=1)/1e3
gen_dispatch_nuclear_2050_t = dispatch_nuclear_2050.generators_t.p.filter(like="nuclear").sum(axis=1)/1e3

fig, axes = plt.subplots(5, 3, figsize=(20, 20))

# Define the data for each technology across years
years = [2030, 2040, 2050]
gen_variable = {
    "solar": [gen_variable_solar_2030_t, gen_variable_solar_2040_t, gen_variable_solar_2050_t],
    "onwind": [gen_variable_onwind_2030_t, gen_variable_onwind_2040_t, gen_variable_onwind_2050_t],
    "offwind": [gen_variable_offwind_2030_t, gen_variable_offwind_2040_t, gen_variable_offwind_2050_t],
    "vre":  [gen_variable_vre_2030_t, gen_variable_vre_2040_t, gen_variable_vre_2050_t],
    "nuclear": [gen_variable_nuclear_2030_t, gen_variable_nuclear_2040_t, gen_variable_nuclear_2050_t]
}

gen_dispatch = {
    "solar": [gen_dispatch_solar_2030_t, gen_dispatch_solar_2040_t, gen_dispatch_solar_2050_t],
    "onwind": [gen_dispatch_onwind_2030_t, gen_dispatch_onwind_2040_t, gen_dispatch_onwind_2050_t],
    "offwind": [gen_dispatch_offwind_2030_t, gen_dispatch_offwind_2040_t, gen_dispatch_offwind_2050_t],
    "vre": [gen_dispatch_vre_2030_t, gen_dispatch_vre_2040_t, gen_dispatch_vre_2050_t],
    "nuclear": [gen_dispatch_nuclear_2030_t, gen_dispatch_nuclear_2040_t, gen_dispatch_nuclear_2050_t]
}
technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

# Loop through each technology and year to plot the data
for row, tech in enumerate(technologies):
    for col, year in enumerate(years):
        # Extract variable generation and dispatchable generation for the current technology and year
        variable_data = gen_variable[tech][col]
        dispatch_data = gen_dispatch[tech][col]

        # Plot the variable generation (using technology-specific color)
        axes[row, col].plot(variable_data, color=colors.get(tech, 'black'), label=f"Variable {tech}")
        
        # Plot the dispatchable generation in black
        axes[row, col].plot(dispatch_data, color='black', label=f"Dispatchable {tech}")
        
        axes[row, col].set_ylim()
        start_of_year = pd.to_datetime('2013-01-01 00:00:00')
        end_of_year = pd.to_datetime('2013-12-31 23:00:00')
        axes[row, col].set_xlim([start_of_year, end_of_year])
        axes[row, col].xaxis.set_major_formatter(mdates.DateFormatter('%b'))
        axes[row, col].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        axes[row, col].set_ylabel("GW", fontsize=15)
        if row == 0:
         axes[row, col].set_title(f"{year}", fontsize=15)
        axes[row, col].tick_params(axis='x', labelsize=15)  # Increase x tick size
        axes[row, col].tick_params(axis='y', labelsize=15) 
        # axes[row, col].legend(loc='upper right', fontsize=15,frameon=True)
        axes[row, col].set_facecolor('white')
        axes[row, col].grid(True,color="lightgray", linestyle="--", linewidth=0.7, alpha=0.8)

legend_elements = [
    Line2D([0], [0], color='#f9d002', lw=6, label="Variable Solar"),
    Line2D([0], [0], color='#235ebc', lw=6, label="Variable Onwind"),
    Line2D([0], [0], color='#6895dd', lw=6, label="Variable Offwind"),
    Line2D([0], [0], color='#baf238', lw=6, label="Variable VRE"),
    Line2D([0], [0], color='#ff8c00', lw=6, label="Variable Nuclear"),
    Line2D([0], [0], color='black', lw=6, label="Dispatchable for each technology")
]

# Add the custom legend to the figure, outside the plot area
plt.legend(handles=legend_elements, fontsize=15, bbox_to_anchor=(1.05, -0.2), ncol=6, frameon=False)
# Adjust layout to prevent overlap
# plt.tight_layout()
# Show the plot
plt.show()

#%%
import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(15, 25))  # Set figure size

# Define layout: Full-year in first column, two small plots stacked in second column
gs = gridspec.GridSpec(5, 2, height_ratios=[1]*5, width_ratios=[1.5, 1], figure=fig)

# Define colors for different technologies
colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}

# Define time ranges
start_full = pd.to_datetime('2013-01-01 00:00:00')
end_full = pd.to_datetime('2013-12-31 23:00:00')

start_winter = pd.to_datetime('2013-01-01 00:00:00')
end_winter = pd.to_datetime('2013-01-07 23:00:00')

start_summer = pd.to_datetime('2013-07-01 00:00:00')
end_summer = pd.to_datetime('2013-07-07 23:00:00')

technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]
fig.patch.set_facecolor('white')
for i, tech in enumerate(technologies):
    variable_data = gen_variable[tech][2]  # Replace with actual data
    dispatch_data = gen_dispatch[tech][2]  # Replace with actual data

    ## **Full-Year Plot (Large, First Column)**
    title_tech = tech.upper() if tech.lower() == "vre" else tech.capitalize()
    ax_main = fig.add_subplot(gs[i, 0])
    ax_main.plot(variable_data, color=colors.get(tech, 'black'))
    ax_main.plot(dispatch_data, color='black',linestyle='-', alpha=0.5)
    ax_main.set_xlim([start_full, end_full])
    ax_main.set_title(f"{title_tech} (2050)", fontsize=20)
    ax_main.set_facecolor('white') 
    ax_main.grid(True)
    ax_main.xaxis.set_major_locator(mdates.MonthLocator())
    ax_main.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
    ax_main.tick_params(axis='x', labelsize=20)  # Increase x-tick size
    ax_main.tick_params(axis='y', labelsize=20)
    ax_main.yaxis.set_major_locator(MaxNLocator(nbins=4,integer=True))
    ax_main.xaxis.set_major_locator(MaxNLocator(nbins=5))
    ax_main.grid(True, color='gray', linestyle='--', linewidth=0.2)
    ax_main.set_ylabel("GW", fontsize=20)
    ## **Small Plots (Stacked in Second Column)**
    gs_sub = gridspec.GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[i, 1], hspace=0.4)  # Create sub-grid for stacking

    # **Winter Plot (Top Small)**
    ax_winter = fig.add_subplot(gs_sub[0])
    ax_winter.plot(variable_data, color=colors.get(tech, 'black'), linestyle="-",linewidth=3,label="Variable Generation")
    ax_winter.plot(dispatch_data, color='black',linewidth=3,label="Dispatched Generation")
    ax_winter.set_xlim([start_winter, end_winter])
    ax_winter.set_title("Winter Week", fontsize=20)
    ax_winter.set_facecolor('white')
    ax_winter.grid(True)
    ax_winter.xaxis.set_major_locator(mdates.DayLocator())
    ax_winter.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    ax_winter.tick_params(axis='x', labelsize=20)
    ax_winter.tick_params(axis='y', labelsize=20)
    ax_winter.yaxis.set_major_locator(MaxNLocator(nbins=4,integer=True))
    ax_winter.grid(True, color='gray', linestyle='--', linewidth=0.2)
    # ax_winter.set_ylabel("MW", fontsize=20)

    # **Summer Plot (Bottom Small)**
    ax_summer = fig.add_subplot(gs_sub[1])
    ax_summer.plot(variable_data, color=colors.get(tech, 'black'), linestyle="-",linewidth=3)
    ax_summer.plot(dispatch_data, color='black',linewidth=3)
    ax_summer.set_xlim([start_summer, end_summer])
    ax_summer.set_title("Summer Week", fontsize=20)
    ax_summer.set_facecolor('white')
    ax_summer.grid(True)
    ax_summer.xaxis.set_major_locator(mdates.DayLocator())
    ax_summer.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
    ax_summer.tick_params(axis='x', labelsize=20)
    ax_summer.tick_params(axis='y', labelsize=20)
    ax_summer.yaxis.set_major_locator(MaxNLocator(nbins=4,integer=True))
    ax_summer.grid(True, color='gray', linestyle='--', linewidth=0.2)
    # ax_summer.set_ylabel("MW", fontsize=20)

plt.tight_layout()
plt.show()

#%%
import matplotlib.gridspec as gridspec
fig = plt.figure(figsize=(22, 14))
fig.patch.set_facecolor("white")

# === OUTER GRID: 2 rows × 3 columns (technologies) ===
gs_outer = gridspec.GridSpec(
    2, 3,
    figure=fig,
    hspace=0.35,
    wspace=0.25
)


# Define colors for different technologies
colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}

# Define time ranges
start_full = pd.to_datetime('2013-01-01 00:00:00')
end_full = pd.to_datetime('2013-12-31 23:00:00')

start_winter = pd.to_datetime('2013-01-01 00:00:00')
end_winter = pd.to_datetime('2013-01-07 23:00:00')

start_summer = pd.to_datetime('2013-07-01 00:00:00')
end_summer = pd.to_datetime('2013-07-07 23:00:00')

technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]
for i, tech in enumerate(technologies):

    row = i // 3
    col = i % 3

    variable_data = gen_variable[tech][2]
    dispatch_data = gen_dispatch[tech][2]

    title_tech = tech.upper() if tech.lower() == "vre" else tech.capitalize()

    # === INNER GRID: full year + winter/summer ===
    gs_inner = gridspec.GridSpecFromSubplotSpec(
        2, 2,
        subplot_spec=gs_outer[row, col],
        height_ratios=[2.2, 1],
        hspace=0.25,
        wspace=0.15
    )
    # ---------- Full year (top, spanning both columns) ----------
    ax_full = fig.add_subplot(gs_inner[0, :])
    ax_full.plot(variable_data, color=colors.get(tech, "black"))
    ax_full.plot(dispatch_data, color="black", alpha=0.5)

    ax_full.set_xlim(start_full, end_full)
    ax_full.set_title(f"{title_tech} (2050)", fontsize=16)
    ax_full.grid(True, color="gray", linestyle="--", linewidth=0.2)

    ax_full.xaxis.set_major_locator(mdates.MonthLocator())
    ax_full.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax_full.tick_params(axis="both", labelsize=12)
    ax_full.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))

    if col == 0:
        ax_full.set_ylabel("GW", fontsize=14)

    # ---------- Winter week (bottom-left) ----------
    ax_winter = fig.add_subplot(gs_inner[1, 0])
    ax_winter.plot(variable_data, color=colors.get(tech, "black"), linewidth=2)
    ax_winter.plot(dispatch_data, color="black", linewidth=2)

    ax_winter.set_xlim(start_winter, end_winter)
    ax_winter.set_title("Winter week", fontsize=13)
    ax_winter.grid(True, color="gray", linestyle="--", linewidth=0.2)

    ax_winter.xaxis.set_major_locator(mdates.DayLocator())
    ax_winter.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    ax_winter.tick_params(axis="both", labelsize=11)
    ax_winter.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))

    # ---------- Summer week (bottom-right) ----------
    ax_summer = fig.add_subplot(gs_inner[1, 1])
    ax_summer.plot(variable_data, color=colors.get(tech, "black"), linewidth=2)
    ax_summer.plot(dispatch_data, color="black", linewidth=2)

    ax_summer.set_xlim(start_summer, end_summer)
    ax_summer.set_title("Summer week", fontsize=13)
    ax_summer.grid(True, color="gray", linestyle="--", linewidth=0.2)

    ax_summer.xaxis.set_major_locator(mdates.DayLocator())
    ax_summer.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
    ax_summer.tick_params(axis="both", labelsize=11)
    ax_summer.yaxis.set_major_locator(MaxNLocator(nbins=3, integer=True))

fig.patch.set_facecolor('white')
plt.tight_layout()
plt.show()
#%%
fig = plt.figure(figsize=(22, 12))
fig.patch.set_facecolor('white')  # Figure background

# Outer grid: 2 rows × 3 columns
gs_outer = gridspec.GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.25)

# Colors
colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}

# Time range: one month
start_month = pd.to_datetime("2013-01-01 00:00:00")
end_month   = pd.to_datetime("2013-01-31 23:00:00")

technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

for i, tech in enumerate(technologies):
    row = i // 3
    col = i % 3

    variable_data = gen_variable[tech][2]
    dispatch_data = gen_dispatch[tech][2]

    title_tech = tech.upper() if tech.lower() == "vre" else tech.capitalize()

    # Add subplot
    ax = fig.add_subplot(gs_outer[row, col])

    ax.plot(variable_data, color=colors.get(tech, 'black'), linewidth=2, label="Variable")
    ax.plot(dispatch_data, color='black', linestyle='-', alpha=0.5, linewidth=2, label="Flexible")

    # X-axis limits for the month
    ax.set_xlim([start_month, end_month])
    ax.set_title(f"{title_tech} (2050)", fontsize=16)

    # White background, no grid
    ax.set_facecolor('white')
    ax.grid(False)

    # X-axis ticks by week
    ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d %b'))

    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=4, integer=True))

    ax.set_ylabel("GW", fontsize=14)

    # Add legend only once
    if i == 0:
        ax.legend(fontsize=12, loc="upper right")

plt.tight_layout()
plt.show()
#%%


    
    
planning_horizons = [2030, 2040, 2050]
discount_rate = 0.07
simpl = ''
cluster = '6'
opt = ''
sector_opt = ''

def build_filename(simpl, cluster, opt, sector_opt, planning_horizon):
    prefix = f"results/reference/networks/base_"
    return f"{prefix}s{simpl}_{cluster}_{opt}_{sector_opt}_{planning_horizon}.nc"

def load_file(filename):
    return pypsa.Network(filename)

def load_files(planning_horizons, simpl, cluster, opt, sector_opt):
    files = {}
    for planning_horizon in planning_horizons:
        filename = build_filename(simpl, cluster, opt, sector_opt, planning_horizon)
        files[planning_horizon] = load_file(filename)
    return files

# Store loaded files per scenario
all_loaded_files = load_files(planning_horizons, simpl, cluster, opt, sector_opt) 
valcoe_dict = {}   
lcoe_dict = {}                
for planning_horizon in planning_horizons:
     fn = f"/home/umair/pypsa-eur_integration_costs/resourcess/reference/costs_2050_processed.csv"
     data = pd.read_csv(fn, index_col=[0, 1]).sort_index()
     solar_inv = float(data.loc[("solar", "investment")]) * 1000
     solar_fom = float(data.loc[("solar", "FOM")])/100
     solar_vom = float(data.loc[("solar", "VOM")])
     solar_life = float(data.loc[("solar", "lifetime")])
     solar_rooftop_inv = float(data.loc[("solar-rooftop", "investment")]) * 1000
     solar_rooftop_fom = float(data.loc[("solar-rooftop", "FOM")])/100
     solar_rooftop_life = float(data.loc[("solar-rooftop", "lifetime")])
     offwind_inv = float(data.loc[("offwind", "investment")]) * 1000
     offwind_fom = float(data.loc[("offwind", "FOM")])/100
     offwind_vom = float(data.loc[("offwind", "VOM")])
     offwind_life = float(data.loc[("offwind", "lifetime")])
     onwind_inv = float(data.loc[("onwind", "investment")]) * 1000
     onwind_fom = float(data.loc[("onwind", "FOM")])/100
     onwind_vom = float(data.loc[("onwind", "VOM")])
     onwind_life = float(data.loc[("onwind", "lifetime")])
     nuc_inv = float(data.loc[("nuclear", "investment")]) * 1000
     nuc_fom = float(data.loc[("nuclear", "FOM")])/100
     nuc_vom = float(data.loc[("nuclear", "VOM")])
     nuc_life = float(data.loc[("nuclear", "lifetime")])
     gas_price = float(data.loc[("gas", "fuel")])
     ura_price = float(data.loc[("nuclear", "fuel")])
     discount_rate = 0.07

     ann_factor_solar = (1 - ((1 + discount_rate) ** -solar_life))
     ann_factor_solar_rooftop = (1 - ((1 + discount_rate) ** -solar_rooftop_life))
     ann_factor_offwind = (1 - ((1 + discount_rate) ** -offwind_life))
     ann_factor_onwind = (1 - ((1 + discount_rate) ** -onwind_life))
     ann_factor_nuc = (1 - ((1 + discount_rate) ** -nuc_life))

    

     n = all_loaded_files[planning_horizon]
     prices_marginal = n.buses_t.marginal_price.loc[:, n.buses.carrier == "AC"]
     prices_marginal = prices_marginal.sum(axis=0)/8760
     prices_marginal = prices_marginal.sum()/6

     generation_solar = n.generators_t.p.filter(like="solar")
     generation_solar = generation_solar.drop(columns=[col for col in generation_solar.columns if "thermal collector" in col])
     generation_solar = generation_solar.sum(axis=1)
     generation_solar_tot = generation_solar.sum().sum()

     generation_offwind = n.generators_t.p.filter(like="offwind")
     generation_offwind = generation_offwind.sum(axis=1)
     generation_offwind_tot = generation_offwind.sum().sum()

     generation_onwind = n.generators_t.p.filter(like="onwind")
     generation_onwind = generation_onwind.sum(axis=1)
     generation_onwind_tot = generation_onwind.sum().sum()

     generation_nuc = n.generators_t.p.filter(like="nuclear")
     generation_nuc = generation_nuc.sum(axis=1)
     generation_nuc_tot = generation_nuc.sum().sum()
     generation_nuc_tot = 0 if generation_nuc_tot < 1000 else generation_nuc_tot

     opt_solar = n.generators.p_nom_opt.filter(like="solar")
     opt_solar = opt_solar.drop([idx for idx in opt_solar.index if "thermal collector" in idx])
     opt_solar = opt_solar.groupby(opt_solar.index).sum().sum()
     solar_opt_inv = opt_solar * solar_inv * discount_rate / ann_factor_solar
     solar_fom_tot = solar_opt_inv * solar_fom / solar_life
     solar_opt_variable = generation_solar_tot * solar_vom
     solar_cost_tot = df_variable.loc['solar', str(planning_horizon)].sum()
     # solar_cost_tot = solar_opt_inv + solar_fom_tot + solar_opt_variable

     opt_offwind = n.generators.p_nom_opt.filter(like="offwind")
     opt_offwind = opt_offwind.groupby(opt_offwind.index).sum().sum()
     offwind_opt_inv = opt_offwind * offwind_inv * discount_rate / ann_factor_offwind
     offwind_fom_tot = offwind_opt_inv * offwind_fom / offwind_life
     offwind_opt_variable = generation_offwind_tot * offwind_vom
     offwind_cost_tot = df_variable.loc['offshore wind', str(planning_horizon)].sum()

     opt_onwind = n.generators.p_nom_opt.filter(like="onwind")
     opt_onwind = opt_onwind.groupby(opt_onwind.index).sum().sum()
     onwind_opt_inv = opt_onwind * onwind_inv * discount_rate / ann_factor_onwind
     onwind_fom_tot = onwind_opt_inv * onwind_fom / onwind_life
     onwind_opt_variable = generation_onwind_tot * onwind_vom
     onwind_cost_tot = df_variable.loc['onshore wind', str(planning_horizon)].sum()

     opt_nuc = n.generators.p_nom_opt.filter(like="nuclear")
     opt_nuc = opt_nuc.groupby(opt_nuc.index).sum().sum()
     nuc_opt_inv = opt_nuc * nuc_inv * discount_rate / ann_factor_nuc
     nuc_fom_tot = nuc_opt_inv  * nuc_fom / nuc_life
     nuc_gen_price = generation_nuc_tot * ura_price
     nuc_opt_variable = generation_nuc_tot * nuc_vom
     nuc_cost_tot = df_variable.loc['nuclear', str(planning_horizon)].sum()
     nuc_cost_tot = 0 if opt_nuc < 100 else nuc_cost_tot


     lcoe_value_solar = (solar_cost_tot/ generation_solar_tot)
     lcoe_value_offwind = (offwind_cost_tot/ generation_offwind_tot)
     lcoe_value_onwind = (onwind_cost_tot/ generation_onwind_tot)
     lcoe_value_nuc = (nuc_cost_tot/ generation_nuc_tot)

     lcoe_dict[planning_horizon] = {
        "solar": lcoe_value_solar,
        "onwind": lcoe_value_onwind,
        "offwind": lcoe_value_offwind,
        "nuclear": lcoe_value_nuc
    }

     assign_locations(n)
     assign_carriers(n)
     carrier = 'AC'
     busesn = n.buses.index[n.buses.carrier.str.contains(carrier)]

     supplyn = pd.DataFrame(index=n.snapshots)
     for c in n.iterate_components(n.branch_components):
       n_port = 4 if c.name == "Link" else 2  # port3
       for i in range(n_port):
           supplyn = pd.concat(
               (
                   supplyn,
                   (-1)
                   * c.pnl["p" + str(i)]
                   .loc[:, c.df.index[c.df["bus" + str(i)].isin(busesn)]]
                   .groupby(c.df.carrier, axis=1)
                   .sum(),
               ),
               axis=1,
           )
     for c in n.iterate_components(n.one_port_components):
       comps = c.df.index[c.df.bus.isin(busesn)]
       supplyn = pd.concat(
           (
               supplyn,
               ((c.pnl["p"].loc[:, comps]).multiply(c.df.loc[comps, "sign"]))
               .groupby(c.df.carrier, axis=1)
               .sum(),
           ),
           axis=1,
       )
       
     supplyn = supplyn.groupby(rename_techs_tyndp, axis=1).sum()

     bothn = supplyn.columns[(supplyn < 0.0).any() & (supplyn > 0.0).any()]

     positive_supplyn = supplyn[bothn]
     negative_supplyn = supplyn[bothn]

     positive_supplyn = positive_supplyn.mask(positive_supplyn < 0.0, 0.0)
     negative_supplyn = negative_supplyn.mask(negative_supplyn > 0.0, 0.0)

     supplyn[bothn] = positive_supplyn

     supplyn = pd.concat((supplyn, negative_supplyn), axis=1)



     threshold = 0.1

     to_dropn = supplyn.columns[(abs(supplyn) < threshold).all()]

     supplyn.index.name = None


    
     supplyn = supplyn.groupby(supplyn.columns, axis=1).sum()


     c_solarn = ((n.generators_t.p_max_pu * n.generators.p_nom_opt) - n.generators_t.p).filter(
        like="solar", axis=1)
     c_solarn = c_solarn.drop(columns=[col for col in c_solarn.columns if "thermal collector" in col])
     c_solarn = c_solarn.sum(axis=1)
     c_onwindn = ((n.generators_t.p_max_pu * n.generators.p_nom_opt) - n.generators_t.p).filter(
        like="onwind", axis=1
     ).sum(axis=1)
     c_offwindn = ((n.generators_t.p_max_pu * n.generators.p_nom_opt) - n.generators_t.p).filter(
        like="offwind", axis=1
     ).sum(axis=1)
    
     supplyn = supplyn.T
     if "solar" in supplyn.index:
      supplyn.loc["solar"] = supplyn.loc["solar"] + c_solarn
      supplyn.loc["solar curtailment"] = -abs(c_solarn)
     if "onshore wind" in supplyn.index:
      supplyn.loc["onshore wind"] = supplyn.loc["onshore wind"] + c_onwindn
      supplyn.loc["onshore curtailment"] = -abs(c_onwindn)
     if "offshore wind" in supplyn.index:
      supplyn.loc["offshore wind"] = supplyn.loc["offshore wind"] + c_offwindn
      supplyn.loc["offshore curtailment"] = -abs(c_offwindn)
     if "H2 pipeline" in supplyn.index:
       supplyn = supplyn.drop('H2 pipeline')
     supplyn = supplyn.T
     if "V2G" in n.carriers.index:
         v2g = n.links_t.p1.filter(like="V2G").sum(axis=1)
         v2g = v2g.to_frame()
         v2g = v2g.rename(columns={v2g.columns[0]: 'V2G'})
         v2g = v2g/1e3
         supplyn['electricity distribution grid'] = supplyn['electricity distribution grid'] + v2g['V2G']
         supplyn['V2G'] = v2g['V2G'].abs()
         
     positive_supplyn = supplyn[supplyn >= 0].fillna(0)
     negative_supplyn = supplyn[supplyn < 0].fillna(0)
     positive_supplyn = positive_supplyn.applymap(lambda x: x if x >= 0.1 else 0)
     negative_supplyn = negative_supplyn.applymap(lambda x: x if x <= -0.1 else 0)
     positive_supplyn = positive_supplyn.loc[:, (positive_supplyn > 0).any()]
     negative_supplyn = negative_supplyn.loc[:, (negative_supplyn < 0).any()]
     positive_supplyn_tot = positive_supplyn.sum(axis=1).sum()
     total_generation = positive_supplyn_tot

     wholesale_prices = n.buses_t.marginal_price.loc[:, n.buses.carrier == "AC"]
     wholesale_prices = wholesale_prices.sum(axis=1)/6
     energy_val_tot = (wholesale_prices * total_generation) / (total_generation)
     energy_val_tot = energy_val_tot.fillna(0).sum()/8760
     energy_val_solar = (wholesale_prices * generation_solar) / (generation_solar)
     energy_val_solar = energy_val_solar.fillna(0).sum()/8760
     energy_val_onwind = (wholesale_prices * generation_onwind) / (generation_onwind)
     energy_val_onwind = energy_val_onwind.fillna(0).sum()/8760
     energy_val_offwind = (wholesale_prices * generation_offwind) / (generation_offwind)
     energy_val_offwind = energy_val_offwind.fillna(0).sum()/8760
     energy_val_nuc = (wholesale_prices * generation_nuc) / (generation_nuc)
     energy_val_nuc = energy_val_nuc.fillna(0).sum()/8760

     load = n.loads_t.p.loc[:, n.loads.carrier.isin([
    "electricity", 
    "industry electricity", 
    "agriculture electricity", 
    "land transport EV",
    # "residential urban decentral heat",
    # "services urban decentral heat"
])].sum(axis=1)
     # peak_demand_30 = {}
# Itead = load.groupby(load.columns.str[:2], axis=1).sum()

# peakrate through each column in the DataFrame
     # for col in load.columns:
     peak_demand = load.dropna().nlargest(30)
#      peak_demand_30 = peak_demand.tolist()
# # Convert the dictionary back into a DataFrame
#      peak_demands = pd.Series(peak_demand_30)
     # solar_gen_peak_hours = pd.Series()
     # onwind_gen_peak_hours = pd.Series()
     # offwind_gen_peak_hours = pd.Series()
     # nuc_gen_peak_hours = pd.Series()
# Iterate over each column in the load DataFrame
     # for col in load.columns:
    # Get the top 30 snapshots for the current column
     top_snapshots = peak_demand.index
     solar_gen_peak_hours = generation_solar.loc[top_snapshots]
     onwind_gen_peak_hours = generation_onwind.loc[top_snapshots]
     offwind_gen_peak_hours = generation_offwind.loc[top_snapshots]
     nuc_gen_peak_hours = generation_nuc.loc[top_snapshots]
       
     capacity_credit_solar = solar_gen_peak_hours / peak_demand
     capacity_credit_solar = capacity_credit_solar.sum()/30
     capacity_credit_onwind = onwind_gen_peak_hours / peak_demand
     capacity_credit_onwind = capacity_credit_onwind.sum()/30
     capacity_credit_offwind = offwind_gen_peak_hours / peak_demand
     capacity_credit_offwind = capacity_credit_offwind.sum()/30
     capacity_credit_nuc = nuc_gen_peak_hours / peak_demand
     capacity_credit_nuc = 1
     basic_capacity_value = 75
     capacity_factor_solar = generation_solar_tot / (opt_solar * 8760)
     capacity_factor_onwind = generation_onwind_tot / (opt_onwind * 8760)
     capacity_factor_offwind = generation_offwind_tot / (opt_offwind * 8760)
     capacity_factor_nuc = generation_nuc_tot / (opt_nuc * 8760)

     capacity_value_solar = (capacity_credit_solar * basic_capacity_value) / (capacity_factor_solar * (8760/1000))
     capacity_value_onwind = (capacity_credit_onwind * basic_capacity_value) / (capacity_factor_onwind * (8760/1000))
     capacity_value_offwind = (capacity_credit_offwind * basic_capacity_value) / (capacity_factor_offwind * (8760/1000))
     capacity_value_nuc = (capacity_credit_nuc * basic_capacity_value) / (capacity_factor_nuc * (8760/1000))
     capacity_value_tot = (1* basic_capacity_value) / (1 * (8760/1000))

     flexibility_value_mul_solar =  (generation_solar / total_generation).sum()/8760
     flexibility_value_solar = (flexibility_value_mul_solar * basic_capacity_value) / (capacity_factor_solar * (8760/1000))
     flexibility_value_mul_onwind =  (generation_onwind / total_generation).sum()/8760
     flexibility_value_onwind = (flexibility_value_mul_onwind * basic_capacity_value) / (capacity_factor_onwind * (8760/1000))
     flexibility_value_mul_offwind =  (generation_offwind / total_generation).sum()/8760
     flexibility_value_offwind = (flexibility_value_mul_offwind * basic_capacity_value) / (capacity_factor_offwind * (8760/1000))
     flexibility_value_mul_nuc =  (generation_nuc / total_generation).sum()/8760
     flexibility_value_nuc = (flexibility_value_mul_nuc * basic_capacity_value) / (capacity_factor_nuc * (8760/1000))
     flexibility_value_tot = (1 * basic_capacity_value) / (1 * (8760/1000))

     valcoe_solar = lcoe_value_solar + (energy_val_tot - energy_val_solar) + (capacity_value_tot - capacity_value_solar) + (flexibility_value_tot - flexibility_value_solar)
     valcoe_onwind = lcoe_value_onwind + (energy_val_tot - energy_val_onwind) + (capacity_value_tot - capacity_value_onwind) + (flexibility_value_tot - flexibility_value_onwind)
     valcoe_offwind = lcoe_value_offwind + (energy_val_tot - energy_val_offwind) + (capacity_value_tot - capacity_value_offwind) + (flexibility_value_tot - flexibility_value_offwind)
     valcoe_nuc = lcoe_value_nuc + (energy_val_tot - energy_val_nuc) + (capacity_value_tot - capacity_value_nuc) + (flexibility_value_tot - flexibility_value_nuc)
     valcoe_nuc = 0 if opt_nuc < 100 else valcoe_nuc
     valcoe_dict[planning_horizon] = {
        "solar": valcoe_solar,
        "onwind": valcoe_onwind,
        "offwind": valcoe_offwind,
        "nuclear": valcoe_nuc
    }

# def build_filename_nuclear(simpl, cluster, opt, sector_opt, ll, planning_horizon):
#     prefix = f"results/variable_overnight_nuclear/postnetworks/elec_"
#     return f"{prefix}s{simpl}_{cluster}_l{ll}_{opt}_{sector_opt}_{planning_horizon}.nc"

# def load_file_nuclear(filename_nuclear):
#     return pypsa.Network(filename_nuclear)

# def load_files_nuclear(planning_horizons, simpl, cluster, opt, sector_opt, ll):
#     files_nuclear = {}
#     for planning_horizon in planning_horizons:
#         filename_nuclear = build_filename_nuclear(simpl, cluster, opt, sector_opt, ll, planning_horizon)
#         files_nuclear[planning_horizon] = load_file_nuclear(filename_nuclear)
#     return files_nuclear

# # Store loaded files per scenario
# all_loaded_files_nuclear = load_files_nuclear(planning_horizons, simpl, cluster, opt, sector_opt, ll) 
# valcoe_dict_nuclear = {}   
# lcoe_dict_nuclear = {}                
# for planning_horizon in planning_horizons:
#      fn = f"/home/umair/pypsa-eur_integration/data/costs_{planning_horizons[0]}.csv"  # Ensure single value
#      data = pd.read_csv(fn, index_col=[0, 1]).sort_index()
#      nuc_inv = data.loc[("nuclear", "investment"), "value"] * 1000
#      nuc_fom = data.loc[("nuclear", "FOM"), "value"]/100
#      nuc_vom = data.loc[("nuclear", "VOM"), "value"]
#      nuc_life = data.loc[("nuclear", "lifetime"), "value"]
#      gas_price = data.loc[("gas", "fuel"), "value"]
#      ura_price = data.loc[("nuclear", "fuel"), "value"]
#      discount_rate = 0.07
#      ann_factor_nuc = (1 - ((1 + discount_rate) ** -nuc_life))

    

#      n = all_loaded_files_nuclear[planning_horizon]
#      prices_marginal_nuclear = n.buses_t.marginal_price.loc[:, n.buses.carrier == "AC"]
#      prices_marginal_nuclear = prices_marginal_nuclear.sum(axis=0)/8760
#      prices_marginal_nuclear = prices_marginal_nuclear.sum()/6

#      generation_nuc = n.links_t.p0.filter(like="nuclear")
#      generation_nuc = generation_nuc.sum(axis=1)
#      generation_nuc_tot = generation_nuc.sum().sum()

#      opt_nuc = n.links.p_nom_opt.filter(like="nuclear")
#      opt_nuc = opt_nuc.groupby(opt_nuc.index).sum().sum()
#      nuc_opt_inv = opt_nuc * nuc_inv * discount_rate / ann_factor_nuc
#      nuc_fom_tot = nuc_opt_inv  * nuc_fom / nuc_life
#      nuc_gen_price = generation_nuc_tot * ura_price
#      nuc_opt_variable = generation_nuc_tot * nuc_vom
#      # nuc_cost_tot = costs_variable_nuclear.loc['nuclear', str(planning_horizon)].sum()
#      nuc_cost_tot = nuc_opt_inv + nuc_fom_tot + nuc_gen_price + nuc_opt_variable

#      lcoe_value_nuc = (nuc_cost_tot/ generation_nuc_tot)
#      # if lcoe_value_nuc < -100 or lcoe_value_nuc > 100:
#      #    lcoe_value_nuc = 0

#      lcoe_dict_nuclear[str(planning_horizon)] = {
#         "nuclear": lcoe_value_nuc
#     }
#      assign_location(n)
#      assign_carriers(n)
#      carrier = 'AC'
#      busesn = n.buses.index[n.buses.carrier.str.contains(carrier)]

#      supplyn = pd.DataFrame(index=n.snapshots)
#      for c in n.iterate_components(n.branch_components):
#        n_port = 4 if c.name == "Link" else 2  # port3
#        for i in range(n_port):
#            supplyn = pd.concat(
#                (
#                    supplyn,
#                    (-1)
#                    * c.pnl["p" + str(i)]
#                    .loc[:, c.df.index[c.df["bus" + str(i)].isin(busesn)]]
#                    .groupby(c.df.carrier, axis=1)
#                    .sum(),
#                ),
#                axis=1,
#            )
#      for c in n.iterate_components(n.one_port_components):
#        comps = c.df.index[c.df.bus.isin(busesn)]
#        supplyn = pd.concat(
#            (
#                supplyn,
#                ((c.pnl["p"].loc[:, comps]).multiply(c.df.loc[comps, "sign"]))
#                .groupby(c.df.carrier, axis=1)
#                .sum(),
#            ),
#            axis=1,
#        )
       
#      supplyn = supplyn.groupby(rename_techs_tyndp, axis=1).sum()

#      bothn = supplyn.columns[(supplyn < 0.0).any() & (supplyn > 0.0).any()]

#      positive_supplyn = supplyn[bothn]
#      negative_supplyn = supplyn[bothn]

#      positive_supplyn = positive_supplyn.mask(positive_supplyn < 0.0, 0.0)
#      negative_supplyn = negative_supplyn.mask(negative_supplyn > 0.0, 0.0)

#      supplyn[bothn] = positive_supplyn

#      supplyn = pd.concat((supplyn, negative_supplyn), axis=1)



#      threshold = 0.1

#      to_dropn = supplyn.columns[(abs(supplyn) < threshold).all()]

#      supplyn.index.name = None


    
#      supplyn = supplyn.groupby(supplyn.columns, axis=1).sum()


#      c_solarn = ((n.generators_t.p_max_pu * n.generators.p_nom_opt) - n.generators_t.p).filter(
#         like="solar", axis=1)
#      c_solarn = c_solarn.drop(columns=[col for col in c_solarn.columns if "thermal collector" in col])
#      c_solarn = c_solarn.sum(axis=1)
#      c_onwindn = ((n.generators_t.p_max_pu * n.generators.p_nom_opt) - n.generators_t.p).filter(
#         like="onwind", axis=1
#      ).sum(axis=1)
#      c_offwindn = ((n.generators_t.p_max_pu * n.generators.p_nom_opt) - n.generators_t.p).filter(
#         like="offwind", axis=1
#      ).sum(axis=1)
    
#      supplyn = supplyn.T
#      if "solar" in supplyn.index:
#       supplyn.loc["solar"] = supplyn.loc["solar"] + c_solarn
#       supplyn.loc["solar curtailment"] = -abs(c_solarn)
#      if "onshore wind" in supplyn.index:
#       supplyn.loc["onshore wind"] = supplyn.loc["onshore wind"] + c_onwindn
#       supplyn.loc["onshore curtailment"] = -abs(c_onwindn)
#      if "offshore wind" in supplyn.index:
#       supplyn.loc["offshore wind"] = supplyn.loc["offshore wind"] + c_offwindn
#       supplyn.loc["offshore curtailment"] = -abs(c_offwindn)
#      if "H2 pipeline" in supplyn.index:
#        supplyn = supplyn.drop('H2 pipeline')
#      supplyn = supplyn.T
#      if "V2G" in n.carriers.index:
#          v2g = n.links_t.p1.filter(like="V2G").sum(axis=1)
#          v2g = v2g.to_frame()
#          v2g = v2g.rename(columns={v2g.columns[0]: 'V2G'})
#          v2g = v2g/1e3
#          supplyn['electricity distribution grid'] = supplyn['electricity distribution grid'] + v2g['V2G']
#          supplyn['V2G'] = v2g['V2G'].abs()
         
#      positive_supplyn = supplyn[supplyn >= 0].fillna(0)
#      negative_supplyn = supplyn[supplyn < 0].fillna(0)
#      positive_supplyn = positive_supplyn.applymap(lambda x: x if x >= 0.1 else 0)
#      negative_supplyn = negative_supplyn.applymap(lambda x: x if x <= -0.1 else 0)
#      positive_supplyn = positive_supplyn.loc[:, (positive_supplyn > 0).any()]
#      negative_supplyn = negative_supplyn.loc[:, (negative_supplyn < 0).any()]
#      positive_supplyn_tot = positive_supplyn.sum(axis=1).sum()
#      total_generation = positive_supplyn_tot

#      wholesale_prices = n.buses_t.marginal_price.loc[:, n.buses.carrier == "AC"]
#      wholesale_prices = wholesale_prices.sum(axis=1)/6
#      energy_val_tot = (wholesale_prices * total_generation) / (total_generation)
#      energy_val_tot = energy_val_tot.fillna(0).sum()/8760
#      energy_val_nuc = (wholesale_prices * generation_nuc) / (generation_nuc)
#      energy_val_nuc = energy_val_nuc.fillna(0).sum()/8760

#      load = n.loads_t.p.loc[:, n.loads.carrier.isin([
#     "electricity", 
#     "industry electricity", 
#     "agriculture electricity", 
#     "land transport EV",
#     # "residential urban decentral heat",
#     # "services urban decentral heat"
# ])].sum(axis=1)
#      # peak_demand_30 = {}
# # Itead = load.groupby(load.columns.str[:2], axis=1).sum()

# # peakrate through each column in the DataFrame
#      # for col in load.columns:
#      peak_demand = load.dropna().nlargest(30)
# #      peak_demand_30 = peak_demand.tolist()
# # # Convert the dictionary back into a DataFrame
# #      peak_demands = pd.Series(peak_demand_30)
#      # solar_gen_peak_hours = pd.Series()
#      # onwind_gen_peak_hours = pd.Series()
#      # offwind_gen_peak_hours = pd.Series()
#      # nuc_gen_peak_hours = pd.Series()
# # Iterate over each column in the load DataFrame
#      # for col in load.columns:
#     # Get the top 30 snapshots for the current column
#      top_snapshots = peak_demand.index
#      nuc_gen_peak_hours = generation_nuc.loc[top_snapshots]
       
#      capacity_credit_nuc = nuc_gen_peak_hours / peak_demand
#      capacity_credit_nuc = 1
#      basic_capacity_value = 75
#      capacity_factor_nuc = generation_nuc_tot / (opt_nuc * 8760)

#      capacity_value_nuc = (capacity_credit_nuc * basic_capacity_value) / (capacity_factor_nuc * (8760/1000))
#      capacity_value_tot = (1* basic_capacity_value) / (1 * (8760/1000))

#      flexibility_value_mul_nuc =  (generation_nuc / total_generation).sum()/8760
#      flexibility_value_nuc = (flexibility_value_mul_nuc * basic_capacity_value) / (capacity_factor_nuc * (8760/1000))
#      flexibility_value_tot = (1 * basic_capacity_value) / (1 * (8760/1000))

#      valcoe_nuc = lcoe_value_nuc + (energy_val_tot - energy_val_nuc) + (capacity_value_tot - capacity_value_nuc) + (flexibility_value_tot - flexibility_value_nuc)
     
#      valcoe_dict_nuclear[planning_horizon] = {
#         "nuclear": valcoe_nuc
#     }

# for year in lcoe_dict_nuclear:
#     if int(year) in lcoe_dict:
#         lcoe_dict[int(year)]['nuclear'] = lcoe_dict_nuclear[year]['nuclear']
        
# for year in valcoe_dict_nuclear:
#     if year in valcoe_dict:
#         valcoe_dict[year]['nuclear'] = valcoe_dict_nuclear[year]['nuclear']
#%%
import copy
inti_costs = {
    "solar": {
        2030: inti_solar_2030,
        2040: inti_solar_2040,
        2050: inti_solar_2050,
    },
    "onwind": {
        2030: inti_onwind_2030,
        2040: inti_onwind_2040,
        2050: inti_onwind_2050,
    },
    "offwind": {
        2030: inti_offwind_2030,
        2040: inti_offwind_2040,
        2050: inti_offwind_2050,
    },
    "nuclear": {
        2030: inti_nuclear_2030,
        2040: inti_nuclear_2040,
        2050: inti_nuclear_2050,
    },

}
lcoe_pypsa = copy.deepcopy(lcoe_dict)
for tech, year_values in inti_costs.items():
  for year, cost in year_values.items():
        if year in lcoe_pypsa:
            # Add the original LCOE value and the calculated inti cost
            lcoe_pypsa[year][tech] = lcoe_pypsa[year].get(tech, 0) + cost
        else:
            # If the year doesn't exist in the LCOE dictionary, create it
            lcoe_pypsa[year] = {tech: cost}

#%%
technologies = ["solar", "onwind", "offwind", "nuclear"]
colors = ["yellow", "blue", "lightblue", "orange"]

# Allowed years for plotting
allowed_years = {2030, 2040, 2050}  # Keep only these years
planning_horizons = sorted([int(year) for year in lcoe_pypsa.keys() if int(year) in allowed_years])

# Plotting the updated LCOE dictionary (with inti_costs added)
fig, ax = plt.subplots(figsize=(15, 7))
fig.patch.set_facecolor('white')  # Set figure background to white
ax.set_facecolor('white')

# Loop through each technology and plot the values
for tech, color in zip(technologies, colors):
    # Get the values for the selected years (2030, 2040, 2050)
    updated_lcoe_values = [lcoe_pypsa[year].get(tech, 0) for year in planning_horizons]
    lcoe_values = [lcoe_dict[year].get(tech, 0) for year in planning_horizons]
    valcoe_values = [valcoe_dict[year].get(tech, 0) for year in planning_horizons]
    # Capitalize the first letter in the technology name for the legend
    tech_name = tech.capitalize()

    # Plot the updated LCOE values (sum of LCOE and inti_costs)
    plt.plot(planning_horizons, updated_lcoe_values, marker='v', markersize=10, linestyle='-', color=color, label=f'Adjusted LCOE {tech_name}')
    plt.plot(planning_horizons, lcoe_values, marker='x', markersize=10, linestyle='--', color=color, label=f'LCOE {tech_name}')
    plt.plot(planning_horizons, valcoe_values, marker='D', markersize=10, linestyle=':', color=color, label=f'VALCOE {tech_name}')
# Labels and legend
plt.ylabel("EUR/MWh", fontsize=15)
plt.xticks(planning_horizons, fontsize=15)  # Increase x-axis tick size
plt.yticks(np.arange(0, 151, 30), fontsize=15)  # Ensure y-axis tick size is readable
plt.legend(fontsize=15, bbox_to_anchor=(1, 1), frameon=False)
plt.grid(True, color='lightgray', linestyle='--')

# Show plot
plt.show()

#%%

technologies = ["solar", "onwind", "offwind", "nuclear"]

colors = ["#f9d002", "#235ebc", "#6895dd", "#ff8c00"]
# Allowed years for plotting
allowed_years = {2030, 2040, 2050}  # Keep only these years
planning_horizons = sorted([int(year) for year in lcoe_pypsa.keys() if int(year) in allowed_years])

# Plotting the updated LCOE dictionary (with inti_costs added)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 10))
fig.patch.set_facecolor('white')  # Set figure background to white

# Flatten the 2x2 axes array for easier iteration
axes = axes.flatten()

# Set the width of the bars
bar_width = 0.2

# Set positions for each technology's bars
x_pos = np.arange(len(planning_horizons))

# Loop through each technology and plot the values
for i, (tech, color) in enumerate(zip(technologies, colors)):
    # Get the values for the selected years (2030, 2040, 2050)
    updated_lcoe_values = [lcoe_pypsa[year].get(tech, 0) for year in planning_horizons]
    lcoe_values = [lcoe_dict[year].get(tech, 0) for year in planning_horizons]
    valcoe_values = [valcoe_dict[year].get(tech, 0) for year in planning_horizons]

    # Capitalize the first letter in the technology name for the legend
    tech_name = tech.capitalize()

    # Plot bars for LCOE values first, then adjusted LCOE (updated LCOE), and finally VALCOE
    ax = axes[i]  # Select the corresponding subplot

    # Plot bars for original LCOE values (this will be the first bar)
    ax.bar(x_pos, lcoe_values, bar_width, color=color,  label='LCOE')

    # Plot bars for updated LCOE (sum of LCOE and inti_costs) - second bar
    ax.bar(x_pos + bar_width, updated_lcoe_values, bar_width,hatch='-', color=color, label='Adjusted LCOE')

    # Plot bars for VALCOE values - third bar
    ax.bar(x_pos + 2*bar_width, valcoe_values, bar_width, color=color, hatch='\\', label='VALCOE')

    # Set the title for each subplot
    ax.set_title(f'{tech_name}', fontsize=15)

    # Set the x-axis labels and ticks
    ax.set_xticks(x_pos + bar_width)  # Shift x-ticks to align with the bars
    ax.set_xticklabels(planning_horizons, fontsize=15)
    # Set the y-axis label and ticks
    ax.set_ylabel("EUR/MWh", fontsize=15)

    # Add a legend to each subplot
    ax.legend(fontsize=15, frameon=False)

    # Enable grid
    ax.grid(True, color='lightgray', linestyle='--')
    ax.set_yticks(np.arange(0, 181, 30))
    ax.tick_params(axis='y', labelsize=15)
    ax.set_facecolor('white')
# Adjust layout
plt.tight_layout()

# Show plot
plt.show()




