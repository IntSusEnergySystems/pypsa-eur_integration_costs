#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 16:27:42 2025

@author: umair
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 12:58:46 2025

@author: umair
"""

import pypsa
import pandas as pd

variable_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/reference/networks/base_s_6___2030.nc")
variable_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/reference/networks/base_s_6___2040.nc")
variable_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/reference/networks/base_s_6___2050.nc")

dispatch_solar_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_solar/networks/base_s_6___2030.nc")
dispatch_solar_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_solar/networks/base_s_6___2040.nc")
dispatch_solar_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_solar/networks/base_s_6___2050.nc")

dispatch_onwind_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_onwind/networks/base_s_6___2030.nc")
dispatch_onwind_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_onwind/networks/base_s_6___2040.nc")
dispatch_onwind_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_onwind/networks/base_s_6___2050.nc")

dispatch_offwind_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_offshore/networks/base_s_6___2030.nc")
dispatch_offwind_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_offshore/networks/base_s_6___2040.nc")
dispatch_offwind_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_offshore/networks/base_s_6___2050.nc")

dispatch_vre_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_vre/networks/base_s_6___2030.nc")
dispatch_vre_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_vre/networks/base_s_6___2040.nc")
dispatch_vre_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_vre/networks/base_s_6___2050.nc")

dispatch_nuclear_2030 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_nuclear/networks/base_s_6___2030.nc")
dispatch_nuclear_2040 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_nuclear/networks/base_s_6___2040.nc")
dispatch_nuclear_2050 = pypsa.Network("/home/umair/pypsa-eur_integration_costs/resultss/flexible_nuclear/networks/base_s_6___2050.nc")


technologies_solar = ["solar","solar rooftop","solar-hasat"]
gen_dispatch_solar_2030 = dispatch_solar_2030.generators_t.p.loc[:, dispatch_solar_2030.generators.carrier.isin(technologies_solar)].sum().sum()
gen_dispatch_solar_2040 = dispatch_solar_2040.generators_t.p.loc[:, dispatch_solar_2040.generators.carrier.isin(technologies_solar)].sum().sum()
gen_dispatch_solar_2050 = dispatch_solar_2050.generators_t.p.loc[:, dispatch_solar_2050.generators.carrier.isin(technologies_solar)].sum().sum()

gen_dispatch_onwind_2030 = dispatch_onwind_2030.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_dispatch_onwind_2040 = dispatch_onwind_2040.generators_t.p.filter(like="onwind").sum(axis=1).sum()
gen_dispatch_onwind_2050 = dispatch_onwind_2050.generators_t.p.filter(like="onwind").sum(axis=1).sum()

technologies_offwind = ["offwind-float", "offwind-ac", "offwind-dc"]
gen_dispatch_offwind_2030 = dispatch_offwind_2030.generators_t.p.loc[:, dispatch_offwind_2030.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_dispatch_offwind_2040 = dispatch_offwind_2040.generators_t.p.loc[:, dispatch_offwind_2040.generators.carrier.isin(technologies_offwind)].sum().sum()
gen_dispatch_offwind_2050 = dispatch_offwind_2050.generators_t.p.loc[:, dispatch_offwind_2050.generators.carrier.isin(technologies_offwind)].sum().sum()

technologies = ["solar","solar rooftop", "onwind", "offwind-float", "offwind-ac", "offwind-dc","solar-hasat"]
gen_dispatch_vre_2030 = dispatch_vre_2030.generators_t.p.loc[:, dispatch_vre_2030.generators.carrier.isin(technologies)].sum().sum()
gen_dispatch_vre_2040 = dispatch_vre_2040.generators_t.p.loc[:, dispatch_vre_2040.generators.carrier.isin(technologies)].sum().sum()
gen_dispatch_vre_2050 = dispatch_vre_2050.generators_t.p.loc[:, dispatch_vre_2050.generators.carrier.isin(technologies)].sum().sum()

gen_dispatch_nuclear_2030 = dispatch_nuclear_2030.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_dispatch_nuclear_2040 = dispatch_nuclear_2040.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
gen_dispatch_nuclear_2050 = dispatch_nuclear_2050.generators_t.p.filter(like="nuclear").sum(axis=1).sum()
#%%


df_variable=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/reference/csvs/costs.csv", index_col=2)
df_variable = df_variable.iloc[:, 2:]
df_variable = df_variable.iloc[3:, :]
df_variable = df_variable.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_variable[['2030', '2040', '2050']] = df_variable[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_variable = df_variable.fillna(0)
df_variable.index.name = 'tech'
df_variable = df_variable.groupby('tech').sum().reset_index()
filtered_df_variable = df_variable[df_variable['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline'])]
filtered_df_variable = filtered_df_variable[['2030', '2040', '2050']].sum()

df_solar=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_solar/csvs/costs.csv", index_col=2)
df_solar = df_solar.iloc[:, 2:]
df_solar = df_solar.iloc[3:, :]
df_solar = df_solar.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_solar[['2030', '2040', '2050']] = df_solar[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_solar = df_solar.fillna(0)
df_solar.index.name = 'tech'
df_solar = df_solar.groupby('tech').sum().reset_index()
filtered_df_solar = df_solar[df_solar['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline'])]
filtered_df_solar = filtered_df_solar[['2030', '2040', '2050']].sum()
grid_solar = filtered_df_variable - filtered_df_solar
generation_solar = pd.Series({'2030': gen_dispatch_solar_2030, '2040': gen_dispatch_solar_2040, '2050': gen_dispatch_solar_2050})

df_onwind=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_onwind/csvs/costs.csv", index_col=2)
df_onwind = df_onwind.iloc[:, 2:]
df_onwind = df_onwind.iloc[3:, :]
df_onwind = df_onwind.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_onwind[['2030', '2040', '2050']] = df_onwind[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_onwind = df_onwind.fillna(0)
df_onwind.index.name = 'tech'
df_onwind = df_onwind.groupby('tech').sum().reset_index()
filtered_df_onwind = df_onwind[df_onwind['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline'])]
filtered_df_onwind = filtered_df_onwind[['2030', '2040', '2050']].sum()
grid_onwind = filtered_df_variable - filtered_df_onwind
generation_onwind = pd.Series({'2030': gen_dispatch_onwind_2030, '2040': gen_dispatch_onwind_2040, '2050': gen_dispatch_onwind_2050})

df_offwind=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_offshore/csvs/costs.csv", index_col=2)
df_offwind = df_offwind.iloc[:, 2:]
df_offwind = df_offwind.iloc[3:, :]
df_offwind = df_offwind.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_offwind[['2030', '2040', '2050']] = df_offwind[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_offwind = df_offwind.fillna(0)
df_offwind.index.name = 'tech'
df_offwind = df_offwind.groupby('tech').sum().reset_index()
filtered_df_offwind = df_offwind[df_offwind['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline'])]
filtered_df_offwind = filtered_df_offwind[['2030', '2040', '2050']].sum()
grid_offwind = filtered_df_variable - filtered_df_offwind
generation_offwind = pd.Series({'2030': gen_dispatch_offwind_2030, '2040': gen_dispatch_offwind_2040, '2050': gen_dispatch_offwind_2050})

df_vre=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_vre/csvs/costs.csv", index_col=2)
df_vre = df_vre.iloc[:, 2:]
df_vre = df_vre.iloc[3:, :]
df_vre = df_vre.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_vre[['2030', '2040', '2050']] = df_vre[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_vre = df_vre.fillna(0)
df_vre.index.name = 'tech'
df_vre = df_vre.groupby('tech').sum().reset_index()
filtered_df_vre = df_vre[df_vre['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline'])]
filtered_df_vre = filtered_df_vre[['2030', '2040', '2050']].sum()
grid_vre = filtered_df_variable - filtered_df_vre
generation_vre = pd.Series({'2030': gen_dispatch_vre_2030, '2040': gen_dispatch_vre_2040, '2050': gen_dispatch_vre_2050})

df_nuclear=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_nuclear/csvs/costs.csv", index_col=2)
df_nuclear = df_nuclear.iloc[:, 2:]
df_nuclear = df_nuclear.iloc[3:, :]
df_nuclear = df_nuclear.rename(columns={'6': '2030','6.1': '2040','6.2': '2050'})
df_nuclear[['2030', '2040', '2050']] = df_nuclear[['2030', '2040', '2050']].apply(pd.to_numeric, errors='coerce')
df_nuclear = df_nuclear.fillna(0)
df_nuclear.index.name = 'tech'
df_nuclear = df_nuclear.groupby('tech').sum().reset_index()
filtered_df_nuclear = df_nuclear[df_nuclear['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline'])]
filtered_df_nuclear = filtered_df_nuclear[['2030', '2040', '2050']].sum()
grid_nuclear = filtered_df_variable - filtered_df_nuclear
generation_nuclear = pd.Series({'2030': gen_dispatch_nuclear_2030, '2040': gen_dispatch_nuclear_2040, '2050': gen_dispatch_nuclear_2050})


grid_costs_solar = grid_solar / generation_solar
grid_costs_onwind = grid_onwind / generation_onwind
grid_costs_offwind = grid_offwind / generation_offwind
grid_costs_vre = grid_vre / generation_vre
grid_costs_nuclear = grid_nuclear / generation_nuclear

import matplotlib.pyplot as plt
tech_colors = {
    "Solar": "#f9d002",
    "Onwind": "#235ebc",
    "Offwind": "#6895dd",
    "VRE": "#baf238",
    "Nuclear": "#ff8c00"
}
grid_costs_df = pd.DataFrame({
    'Solar': grid_costs_solar,
    'Onwind': grid_costs_onwind,
    'Offwind': grid_costs_offwind,
    'VRE': grid_costs_vre,
    'Nuclear': grid_costs_nuclear
})

colors = [tech_colors[tech] for tech in grid_costs_df.columns]

grid_costs_df.plot(kind='bar', figsize=(10, 6), color=colors)
plt.ylabel("Grid Costs [€/MWh]", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=15)
plt.xticks(rotation=0)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.tight_layout()
plt.show()

#%%
storage_df_variable = df_variable[df_variable['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
                                                            'rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
                                                            'urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
storage_df_variable = storage_df_variable[['2030', '2040', '2050']].sum()

storage_df_solar = df_solar[df_solar['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
                                                            'rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
                                                            'urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
storage_df_solar = storage_df_solar[['2030', '2040', '2050']].sum()
storage_solar = storage_df_variable - storage_df_solar

storage_df_onwind = df_onwind[df_onwind['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
                                                            'rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
                                                            'urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
storage_df_onwind = storage_df_onwind[['2030', '2040', '2050']].sum()
storage_onwind = storage_df_variable - storage_df_onwind

storage_df_offwind = df_offwind[df_offwind['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
                                                            'rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
                                                            'urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
storage_df_offwind = storage_df_offwind[['2030', '2040', '2050']].sum()
storage_offwind = storage_df_variable - storage_df_offwind

storage_df_vre = df_vre[df_vre['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
                                                            'rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
                                                            'urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
storage_df_vre = storage_df_vre[['2030', '2040', '2050']].sum()
storage_vre = storage_df_variable - storage_df_vre

storage_df_nuclear = df_nuclear[df_nuclear['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
                                                            'rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
                                                            'urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
storage_df_nuclear = storage_df_nuclear[['2030', '2040', '2050']].sum()
storage_nuclear = storage_df_variable - storage_df_nuclear

storage_costs_solar = storage_solar / generation_solar
storage_costs_onwind = storage_onwind / generation_onwind
storage_costs_offwind = storage_offwind / generation_offwind
storage_costs_vre = storage_vre / generation_vre
storage_costs_nuclear = storage_nuclear / generation_nuclear

import matplotlib.pyplot as plt
tech_colors = {
    "Solar": "#f9d002",
    "Onwind": "#235ebc",
    "Offwind": "#6895dd",
    "VRE": "#baf238",
    "Nuclear": "#ff8c00"
}
grid_costs_df = pd.DataFrame({
    'Solar': storage_costs_solar,
    'Onwind': storage_costs_onwind,
    'Offwind': storage_costs_offwind,
    'VRE': storage_costs_vre,
    'Nuclear': storage_costs_nuclear
})

colors = [tech_colors[tech] for tech in grid_costs_df.columns]

grid_costs_df.plot(kind='bar', figsize=(10, 6), color=colors)
plt.ylabel("storage Costs [€/MWh]", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=15)
plt.xticks(rotation=0)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.tight_layout()
plt.show()

#%%
# fuel_techs = ['uranium', 'gas', 'coal', 'oil', 'H2', 'NH3', 'lignite', 'solid biomass']
# fn = "/home/umair/pypsa-eur_integration/data/costs_2030.csv"
# data = pd.read_csv(fn, index_col=[0, 1]).sort_index()

# variable_fuels_pp = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/variable_overnight/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# variable_fuels_pp = variable_fuels_pp.drop(2020)
# coal_costs_variable = variable_fuels_pp['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_variable = variable_fuels_pp['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_variable = variable_fuels_pp['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_variable = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/variable_overnight/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_var = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_var = total_h2_cost_var / hours_per_year  # €/MWh
#     h2_prices_variable[year] = avg_h2_price_var
# h2_prices_series_var = pd.Series(h2_prices_variable)
# H2_costs_variable = variable_fuels_pp['Hydrogen network'] * 1e6 * h2_prices_series_var 
# oil_costs_variable = variable_fuels_pp['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_variable = pd.DataFrame({
#     "coal_pp": coal_costs_variable,
#     "biomass_pp": biomass_costs_variable,
#     "gas_pp": gas_costs_variable,
#     "hydrogen_pp": H2_costs_variable,
#     "oil_pp": oil_costs_variable
# })
# fuel_costs_variable = fuel_costs_variable.T[[2030, 2040, 2050]].sum()
# fuel_costs_variable.index = fuel_costs_variable.index.astype(str) 
# fuel_sum = df_variable[df_variable['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum['2030']],
#     '2040': [fuel_sum['2040']],
#     '2050': [fuel_sum['2050']]
# })
# df_variable = df_variable[~df_variable['tech'].isin(fuel_techs)]
# df_variable = pd.concat([df_variable, fuel_row], ignore_index=True)
# fuels_index = df_variable[df_variable['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_variable.at[fuels_index, year] -= fuel_costs_variable[year]

# df_variable = df_variable[~df_variable['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_variable_pp = df_variable[df_variable['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_variable_pp = filtered_df_variable_pp[['2030', '2040', '2050']].sum() + fuel_costs_variable

# variable_fuels_pp_nuclear = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/variable_overnight_nuclear/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# variable_fuels_pp_nuclear = variable_fuels_pp_nuclear.drop(2020)
# coal_costs_variable_nuclear = variable_fuels_pp_nuclear['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_variable_nuclear = variable_fuels_pp_nuclear['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_variable_nuclear = variable_fuels_pp_nuclear['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_variable_nuclear = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/variable_overnight_nuclear/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_var_nuclear = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_var_nuclear = total_h2_cost_var_nuclear / hours_per_year  # €/MWh
#     h2_prices_variable_nuclear[year] = avg_h2_price_var_nuclear
# h2_prices_series_var_nuclear = pd.Series(h2_prices_variable_nuclear)
# H2_costs_variable_nuclear = variable_fuels_pp_nuclear['Hydrogen network'] * 1e6 * h2_prices_series_var_nuclear 
# oil_costs_variable_nuclear = variable_fuels_pp_nuclear['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_variable_nuclear = pd.DataFrame({
#     "coal_pp": coal_costs_variable_nuclear,
#     "biomass_pp": biomass_costs_variable_nuclear,
#     "gas_pp": gas_costs_variable_nuclear,
#     "hydrogen_pp": H2_costs_variable_nuclear,
#     "oil_pp": oil_costs_variable_nuclear
# })
# fuel_costs_variable_nuclear = fuel_costs_variable_nuclear.T[[2030, 2040, 2050]].sum()
# fuel_costs_variable_nuclear.index = fuel_costs_variable_nuclear.index.astype(str) 
# fuel_sum_nuclear = df_variable_nuclear[df_variable_nuclear['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row_nuclear = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum_nuclear['2030']],
#     '2040': [fuel_sum_nuclear['2040']],
#     '2050': [fuel_sum_nuclear['2050']]
# })
# df_variable_nuclear = df_variable_nuclear[~df_variable_nuclear['tech'].isin(fuel_techs)]
# df_variable_nuclear = pd.concat([df_variable_nuclear, fuel_row_nuclear], ignore_index=True)
# fuels_index_nuclear = df_variable_nuclear[df_variable_nuclear['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_variable_nuclear.at[fuels_index_nuclear, year] -= fuel_costs_variable_nuclear[year]

# df_variable_nuclear = df_variable_nuclear[~df_variable_nuclear['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_variable_pp_nuclear = df_variable_nuclear[df_variable_nuclear['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_variable_pp_nuclear = filtered_df_variable_pp_nuclear[['2030', '2040', '2050']].sum() + fuel_costs_variable_nuclear


# solar_fuels_pp = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/dispatch_solar_overnight/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# solar_fuels_pp = solar_fuels_pp.drop(2020)
# coal_costs_solar = solar_fuels_pp['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_solar = solar_fuels_pp['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_solar = solar_fuels_pp['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_solar = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/dispatch_solar_overnight/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_solar = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_solar = total_h2_cost_solar / hours_per_year  # €/MWh
#     h2_prices_solar[year] = avg_h2_price_solar
# h2_prices_series_solar = pd.Series(h2_prices_solar)
# H2_costs_solar = solar_fuels_pp['Hydrogen network'] * 1e6 * h2_prices_series_solar 
# oil_costs_solar = solar_fuels_pp['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_solar = pd.DataFrame({
#     "coal_pp": coal_costs_solar,
#     "biomass_pp": biomass_costs_solar,
#     "gas_pp": gas_costs_solar,
#     "hydrogen_pp": H2_costs_solar,
#     "oil_pp": oil_costs_solar
# })
# fuel_costs_solar = fuel_costs_solar.T[[2030, 2040, 2050]].sum()
# fuel_costs_solar.index = fuel_costs_solar.index.astype(str)
# fuel_sum_solar = df_solar[df_solar['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row_solar = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum_solar['2030']],
#     '2040': [fuel_sum_solar['2040']],
#     '2050': [fuel_sum_solar['2050']]
# })
# df_solar = df_solar[~df_solar['tech'].isin(fuel_techs)]
# df_solar = pd.concat([df_solar, fuel_row_solar], ignore_index=True)
# fuels_index_solar = df_solar[df_solar['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_solar.at[fuels_index_solar, year] -= fuel_costs_solar[year] 

# df_solar = df_solar[~df_solar['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_solar_pp = df_solar[df_solar['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_solar_pp = filtered_df_solar_pp[['2030', '2040', '2050']].sum() + fuel_costs_solar
# pp_solar = filtered_df_variable_pp - filtered_df_solar_pp

# onwind_fuels_pp = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/dispatch_onwind_overnight/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# onwind_fuels_pp = onwind_fuels_pp.drop(2020)
# coal_costs_onwind = onwind_fuels_pp['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_onwind = onwind_fuels_pp['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_onwind = onwind_fuels_pp['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_onwind = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/dispatch_onwind_overnight/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_onwind = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_onwind = total_h2_cost_onwind / hours_per_year  # €/MWh
#     h2_prices_onwind[year] = avg_h2_price_onwind
# h2_prices_series_onwind = pd.Series(h2_prices_onwind)
# H2_costs_onwind = onwind_fuels_pp['Hydrogen network'] * 1e6 * h2_prices_series_onwind 
# oil_costs_onwind = onwind_fuels_pp['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_onwind = pd.DataFrame({
#     "coal_pp": coal_costs_onwind,
#     "biomass_pp": biomass_costs_onwind,
#     "gas_pp": gas_costs_onwind,
#     "hydrogen_pp": H2_costs_onwind,
#     "oil_pp": oil_costs_onwind
# })
# fuel_costs_onwind = fuel_costs_onwind.T[[2030, 2040, 2050]].sum()
# fuel_costs_onwind.index = fuel_costs_onwind.index.astype(str) 
# fuel_sum_onwind = df_onwind[df_onwind['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row_onwind = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum_onwind['2030']],
#     '2040': [fuel_sum_onwind['2040']],
#     '2050': [fuel_sum_onwind['2050']]
# })
# df_onwind = df_onwind[~df_onwind['tech'].isin(fuel_techs)]
# df_onwind = pd.concat([df_onwind, fuel_row_onwind], ignore_index=True)
# fuels_index_onwind = df_onwind[df_onwind['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_onwind.at[fuels_index_onwind, year] -= fuel_costs_onwind[year] 

# df_onwind = df_onwind[~df_onwind['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_onwind_pp = df_onwind[df_onwind['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_onwind_pp = filtered_df_onwind_pp[['2030', '2040', '2050']].sum() + fuel_costs_onwind
# pp_onwind = filtered_df_variable_pp - filtered_df_onwind_pp

# offwind_fuels_pp = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/dispatch_offwind_overnight/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# offwind_fuels_pp = offwind_fuels_pp.drop(2020)
# coal_costs_offwind = offwind_fuels_pp['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_offwind = offwind_fuels_pp['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_offwind = offwind_fuels_pp['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_offwind = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/dispatch_offwind_overnight/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_offwind = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_offwind = total_h2_cost_offwind / hours_per_year  # €/MWh
#     h2_prices_offwind[year] = avg_h2_price_offwind
# h2_prices_series_offwind = pd.Series(h2_prices_offwind)
# H2_costs_offwind = offwind_fuels_pp['Hydrogen network'] * 1e6 * h2_prices_series_offwind 
# oil_costs_offwind = offwind_fuels_pp['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_offwind = pd.DataFrame({
#     "coal_pp": coal_costs_offwind,
#     "biomass_pp": biomass_costs_offwind,
#     "gas_pp": gas_costs_offwind,
#     "hydrogen_pp": H2_costs_offwind,
#     "oil_pp": oil_costs_offwind
# })
# fuel_costs_offwind = fuel_costs_offwind.T[[2030, 2040, 2050]].sum()
# fuel_costs_offwind.index = fuel_costs_offwind.index.astype(str) 
# fuel_sum_offwind = df_offwind[df_offwind['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row_offwind = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum_offwind['2030']],
#     '2040': [fuel_sum_offwind['2040']],
#     '2050': [fuel_sum_offwind['2050']]
# })
# df_offwind = df_offwind[~df_offwind['tech'].isin(fuel_techs)]
# df_offwind = pd.concat([df_offwind, fuel_row_offwind], ignore_index=True)
# fuels_index_offwind = df_offwind[df_offwind['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_offwind.at[fuels_index_offwind, year] -= fuel_costs_offwind[year] 

# df_offwind = df_offwind[~df_offwind['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_offwind_pp = df_offwind[df_offwind['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_offwind_pp = filtered_df_offwind_pp[['2030', '2040', '2050']].sum() + fuel_costs_offwind
# pp_offwind = filtered_df_variable_pp - filtered_df_offwind_pp

# vre_fuels_pp = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/dispatch_vre_overnight/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# vre_fuels_pp = vre_fuels_pp.drop(2020)
# coal_costs_vre = vre_fuels_pp['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_vre = vre_fuels_pp['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_vre = vre_fuels_pp['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_vre = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/dispatch_vre_overnight/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_vre = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_vre = total_h2_cost_vre / hours_per_year  # €/MWh
#     h2_prices_vre[year] = avg_h2_price_vre
# h2_prices_series_vre = pd.Series(h2_prices_vre)
# H2_costs_vre = vre_fuels_pp['Hydrogen network'] * 1e6 * h2_prices_series_vre 
# oil_costs_vre = vre_fuels_pp['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_vre = pd.DataFrame({
#     "coal_pp": coal_costs_vre,
#     "biomass_pp": biomass_costs_vre,
#     "gas_pp": gas_costs_vre,
#     "hydrogen_pp": H2_costs_vre,
#     "oil_pp": oil_costs_vre
# })
# fuel_costs_vre = fuel_costs_vre.T[[2030, 2040, 2050]].sum()
# fuel_costs_vre.index = fuel_costs_vre.index.astype(str) 
# fuel_sum_vre = df_vre[df_vre['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row_vre = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum_vre['2030']],
#     '2040': [fuel_sum_vre['2040']],
#     '2050': [fuel_sum_vre['2050']]
# })
# df_vre = df_vre[~df_vre['tech'].isin(fuel_techs)]
# df_vre = pd.concat([df_vre, fuel_row_vre], ignore_index=True)
# fuels_index_vre = df_vre[df_vre['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_vre.at[fuels_index_vre, year] -= fuel_costs_vre[year] 

# df_vre = df_vre[~df_vre['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_vre_pp = df_vre[df_vre['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_vre_pp = filtered_df_vre_pp[['2030', '2040', '2050']].sum() + fuel_costs_vre
# pp_vre = filtered_df_variable_pp - filtered_df_vre_pp

# nuclear_fuels_pp = pd.read_excel("/home/umair/pypsa-eur_integration/resultss/dispatch_nuclear_overnight/htmls/ChartData_EU.xlsx",sheet_name="Chart 22", index_col=0,skiprows=2)
# nuclear_fuels_pp = nuclear_fuels_pp.drop(2020)
# coal_costs_nuclear = nuclear_fuels_pp['Coal'] * 1e6 * data.loc[("coal", "fuel"), "value"]
# biomass_costs_nuclear = nuclear_fuels_pp['Solid biomass'] * 1e6 * data.loc[("solid biomass", "fuel"), "value"]
# gas_costs_nuclear = nuclear_fuels_pp['Gas grid'] * 1e6 * data.loc[("gas", "fuel"), "value"]
# h2_prices_nuclear = {}
# years = [2030, 2040, 2050]
# hours_per_year = 6 * 8760
# for year in years:
#     path = f"/home/umair/pypsa-eur_integration/resultss/dispatch_nuclear_overnight/postnetworks/elec_s_6_lvopt__1H-T-H-B-I-A-dist1_{year}.nc"
#     network = pypsa.Network(path)
#     total_h2_cost_nuclear = network.buses_t.marginal_price.filter(like="H2").sum().sum()
#     avg_h2_price_nuclear = total_h2_cost_nuclear / hours_per_year  # €/MWh
#     h2_prices_nuclear[year] = avg_h2_price_nuclear
# h2_prices_series_nuclear = pd.Series(h2_prices_nuclear)
# H2_costs_nuclear = nuclear_fuels_pp['Hydrogen network'] * 1e6 * h2_prices_series_nuclear 
# oil_costs_nuclear = nuclear_fuels_pp['Petroleum'] * 1e6 * data.loc[("oil", "fuel"), "value"]
# fuel_costs_nuclear = pd.DataFrame({
#     "coal_pp": coal_costs_nuclear,
#     "biomass_pp": biomass_costs_nuclear,
#     "gas_pp": gas_costs_nuclear,
#     "hydrogen_pp": H2_costs_nuclear,
#     "oil_pp": oil_costs_nuclear
# })
# fuel_costs_nuclear = fuel_costs_nuclear.T[[2030, 2040, 2050]].sum()
# fuel_costs_nuclear.index = fuel_costs_nuclear.index.astype(str)
# fuel_sum_nuclear = df_nuclear[df_nuclear['tech'].isin(fuel_techs)][['2030','2040','2050']].sum()
# fuel_row_nuclear = pd.DataFrame({
#     'tech': ['fuels'],
#     '2030': [fuel_sum_nuclear['2030']],
#     '2040': [fuel_sum_nuclear['2040']],
#     '2050': [fuel_sum_nuclear['2050']]
# })
# df_nuclear = df_nuclear[~df_nuclear['tech'].isin(fuel_techs)]
# df_nuclear = pd.concat([df_nuclear, fuel_row_nuclear], ignore_index=True)
# fuels_index_nuclear = df_nuclear[df_nuclear['tech'] == 'fuels'].index[0]
# for year in ['2030', '2040', '2050']:
#     df_nuclear.at[fuels_index_nuclear, year] -= fuel_costs_nuclear[year]  

# df_nuclear = df_nuclear[~df_nuclear['tech'].isin(['AC', 'DC', 'electricity distribution grid','H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new'])]
# filtered_df_nuclear_pp = df_nuclear[df_nuclear['tech'].isin(['CCGT','H2 Fuel Cell','H2 turbine','OCGT','PHS','hydro','nuclear','offwind','offwind-ac','offwind-dc','onwind','solar','solar rooftop','urban central gas CHP','urban central gas CHP CC','urban central solid biomass CHP','urban central solid biomass CHP CC'])]
# filtered_df_nuclear_pp = filtered_df_nuclear_pp[['2030', '2040', '2050']].sum() + fuel_costs_nuclear
# pp_nuclear = filtered_df_variable_pp_nuclear - filtered_df_nuclear_pp
# # pp_nuclear[(pp_nuclear < -100) | (pp_nuclear > 100)] = 0


# pp_costs_solar = pp_solar / generation_solar
# pp_costs_onwind = pp_onwind / generation_onwind
# pp_costs_offwind = pp_offwind / generation_offwind
# pp_costs_vre = pp_vre / generation_vre
# pp_costs_nuclear = pp_nuclear / generation_nuclear

# pp_costs_df = pd.DataFrame({
#     'Solar': pp_costs_solar,
#     'Onwind': pp_costs_onwind,
#     'Offwind': pp_costs_offwind,
#     'VRE': pp_costs_vre,
#     'Nuclear': pp_costs_nuclear
# })

# colors = [tech_colors[tech] for tech in pp_costs_df.columns]

# pp_costs_df.plot(kind='bar', figsize=(10, 6), color=colors)
# plt.ylabel("Powerplant & CHP Costs [€/MWh]", fontsize=15)
# plt.grid(axis='y', linestyle='--', alpha=0.7)
# plt.xticks(fontsize=15)
# plt.xticks(rotation=0)
# plt.yticks(fontsize=15)
# plt.legend(fontsize=15)
# plt.tight_layout()
# plt.show()


#%%
df_variable = df_variable[~df_variable['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
       'AC', 'DC', 'electricity distribution grid','rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
       'H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline''urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
df_solar = df_solar[~df_solar['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
       'AC', 'DC', 'electricity distribution grid','rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
       'H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline''urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
df_onwind = df_onwind[~df_onwind['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
       'AC', 'DC', 'electricity distribution grid','rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
       'H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline''urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
df_offwind = df_offwind[~df_offwind['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
       'AC', 'DC', 'electricity distribution grid','rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
       'H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline''urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
df_vre = df_vre[~df_vre['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
       'AC', 'DC', 'electricity distribution grid','rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
       'H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline''urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]
df_nuclear = df_nuclear[~df_nuclear['tech'].isin(['battery', 'battery charger', 'battery discharger','home battery', 'home battery charger','home battery discharger','BEV charger','H2 Store','ammonia store','co2 sequestered','co2 stored','co2 vent','rural water tanks',
       'AC', 'DC', 'electricity distribution grid','rural water tanks charger','rural water tanks discharger','urban central water pits', 'urban central water pits charger', 'urban central water pits discharger', 'urban central water tanks','urban central water tanks charger',
       'H2 pipeline','H2 pipeline retrofitted','gas pipeline','gas pipeline new','CO2 pipeline''urban central water tanks discharger','urban decentral water tanks', 'urban decentral water tanks charger','urban decentral water tanks discharger'])]

filtered_df_variable_flex = df_variable[['2030', '2040', '2050']].sum()

filtered_df_solar_flex = df_solar[['2030', '2040', '2050']].sum()
flex_solar = filtered_df_variable_flex - filtered_df_solar_flex

filtered_df_onwind_flex = df_onwind[['2030', '2040', '2050']].sum()
flex_onwind = filtered_df_variable_flex - filtered_df_onwind_flex

filtered_df_offwind_flex = df_offwind[['2030', '2040', '2050']].sum()
flex_offwind = filtered_df_variable_flex - filtered_df_offwind_flex

filtered_df_vre_flex = df_vre[['2030', '2040', '2050']].sum()
flex_vre = filtered_df_variable_flex - filtered_df_vre_flex

filtered_df_nuclear_flex = df_nuclear[['2030', '2040', '2050']].sum()
flex_nuclear = filtered_df_variable_flex - filtered_df_nuclear_flex

flex_costs_solar = flex_solar / generation_solar
flex_costs_onwind = flex_onwind / generation_onwind
flex_costs_offwind = flex_offwind / generation_offwind
flex_costs_vre = flex_vre / generation_vre
flex_costs_nuclear = flex_nuclear / generation_nuclear
# flex_costs_nuclear[(flex_costs_nuclear < -100) | (flex_costs_nuclear > 100)] = 0

flex_costs_df = pd.DataFrame({
    'Solar': flex_costs_solar,
    'Onwind': flex_costs_onwind,
    'Offwind': flex_costs_offwind,
    'VRE': flex_costs_vre,
    'Nuclear': flex_costs_nuclear
})

colors = [tech_colors[tech] for tech in flex_costs_df.columns]

flex_costs_df.plot(kind='bar', figsize=(10, 6), color=colors)
plt.ylabel("Other Costs [€/MWh]", fontsize=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(fontsize=15)
plt.xticks(rotation=0)
plt.yticks(fontsize=15)
plt.legend(fontsize=15)
plt.tight_layout()
plt.show()

#%%
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
    # if "heat pump" in tech or "resistive heater" in tech:
    #     return "power-to-heat"
    if tech in ["H2 Electrolysis", "methanation", 'methanolisation',"helmeth", "H2 liquefaction"]:
        return "power-to-gas"
    elif "H2 pipeline" in tech:
        return "H2 pipeline"
    elif tech in ["nuclear", "uranium"]:
        return "nuclear"
    # elif tech in [ "CHP", "H2 Fuel Cell"]:
    #     return "CHP"
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


df_variable=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/reference/csvs/costs.csv", index_col=2)
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

df_solar=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_solar/csvs/costs.csv", index_col=2)
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


df_onwind=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_onwind/csvs/costs.csv", index_col=2)
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

df_offwind=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_offshore/csvs/costs.csv", index_col=2)
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

df_vre=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_vre/csvs/costs.csv", index_col=2)
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

df_nuclear=pd.read_csv("/home/umair/pypsa-eur_integration_costs/resultss/flexible_nuclear/csvs/costs.csv", index_col=2)
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


planning_horizons = [2030, 2040, 2050]
discount_rate = 0.07
simpl = ''
cluster = '6'
opt = ''
sector_opt = ''

def build_filename(simpl, cluster, opt, sector_opt, planning_horizon):
    prefix = f"resultss/reference/networks/base_"
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
     fn = f"/home/umair/pypsa-eur_integration_costs/resources/reference/costs_2050_processed.csv"  # Ensure single value
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
     lcoe_value_vre = (lcoe_value_solar + lcoe_value_offwind + lcoe_value_onwind) /3
     lcoe_value_nuc = (nuc_cost_tot/ generation_nuc_tot)

     lcoe_dict[str(planning_horizon)] = {
        "Solar": lcoe_value_solar,
        "Onwind": lcoe_value_onwind,
        "Offwind": lcoe_value_offwind,
        "VRE": lcoe_value_vre,
        "Nuclear": lcoe_value_nuc
    }
            
import copy
# def clean(value):
#     return value if -100 <= value <= 100 else 0     
inti_costs = {
    "Solar": {
        '2030': inti_solar_2030,
        '2040': inti_solar_2040,
        '2050': inti_solar_2050,
    },
    "Onwind": {
        '2030': inti_onwind_2030,
        '2040': inti_onwind_2040,
        '2050': inti_onwind_2050,
    },
    "Offwind": {
        '2030': inti_offwind_2030,
        '2040': inti_offwind_2040,
        '2050': inti_offwind_2050,
    },
    "VRE": {
        '2030': inti_vre_2030,
       '2040': inti_vre_2040,
        '2050': inti_vre_2050,
    },
    "Nuclear": {
        '2030': inti_nuclear_2030,
        '2040': inti_nuclear_2040,
        '2050': inti_nuclear_2050,
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
import numpy as np
grid_costs = {
    "Solar": grid_costs_solar.to_dict(),
    "Onwind": grid_costs_onwind.to_dict(),
    "Offwind": grid_costs_offwind.to_dict(),
    "VRE": grid_costs_vre.to_dict(),
    "Nuclear": grid_costs_nuclear.to_dict()
}
other_costs = {
    "Solar": flex_costs_solar.to_dict(),
    "Onwind": flex_costs_onwind.to_dict(),
    "Offwind": flex_costs_offwind.to_dict(),
    "VRE": flex_costs_vre.to_dict(),
    "Nuclear": flex_costs_nuclear.to_dict()
}
storage_costs = {
    "Solar": storage_costs_solar.to_dict(),
    "Onwind": storage_costs_onwind.to_dict(),
    "Offwind": storage_costs_offwind.to_dict(),
    "VRE": storage_costs_vre.to_dict(),
    "Nuclear": storage_costs_nuclear.to_dict()
}
years = ['2030', '2040', '2050']
technologies = ['Solar', 'Onwind', 'Offwind', 'VRE', 'Nuclear']
width = 0.2

fig, axes = plt.subplots(1, len(years), figsize=(18, 6), sharey=True)

for i, year in enumerate(years):
    ax = axes[i]
    x = np.arange(len(technologies))
    
    # Extract base and final LCOE
    base = [lcoe_dict[year][tech] for tech in technologies]
    lcpE = [lcoe_pypsa[year][tech] for tech in technologies]
    
    # Individual cost components
    grid = [grid_costs[tech][year] for tech in technologies]
    other = [other_costs[tech][year] for tech in technologies]
    storage = [storage_costs[tech][year] for tech in technologies]

    # Bars
    ax.bar(x - width, base, width, label='LCOE', color='lightblue')
    ax.bar(x, grid, width, bottom=base, label='grid investments', color='orange')
    ax.bar(x, other, width, bottom=np.array(base)+np.array(grid), label='other investments', color='green')
    ax.bar(x, storage, width, bottom=np.array(base)+np.array(grid)+np.array(other), label='strorage investments', color='red')
    ax.bar(x + width, lcpE, width, label='LCOE PyPSA', color='blue')

    ax.set_xticks(x)
    ax.set_xticklabels(technologies, rotation=45, fontsize=10)
    ax.set_title(f"{year}", fontsize=14)
    ax.set_ylabel("€/MWh")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

# Shared legend
handles, labels = ax.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=4)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()


#%%
years = ['2030', '2040', '2050']
technologies = ['Solar', 'Onwind', 'Offwind', 'VRE', 'Nuclear']
width = 0.15

fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharey=True)
axes = axes.flatten()

for i, tech in enumerate(technologies):
    ax = axes[i]
    x = np.arange(len(years))

    base = np.array([lcoe_dict[year][tech] for year in years])
    grid = np.array([grid_costs[tech][year] for year in years])
    other = np.array([other_costs[tech][year] for year in years])
    storage = np.array([storage_costs[tech][year] for year in years])
    lcpE = np.array([lcoe_pypsa[year][tech] for year in years])

    ax.bar(x - 2*width, base, width, color='lightblue', label='LCOE')
    ax.bar(x - width, grid, width, bottom=base, color='orange', label='Grid Investments')
    ax.bar(x, other, width, bottom=base + grid, color='green', label='Other Investlents')
    ax.bar(x + width, storage, width, bottom=base + grid + other, color='red', label='Storage Investments')
    ax.bar(x + 2*width, lcpE, width, color='blue', label='Adjusted LCOE')

    ax.set_xticks(x)
    ax.set_xticklabels(years)
    ax.set_title(tech,fontsize=15)
    ax.tick_params(axis='both', labelsize=15)
    if i % 3 == 0:
        ax.set_ylabel("€/MWh", fontsize=15)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

# Use the 6th subplot (last one) for the legend
legend_ax = axes[-1]
legend_ax.axis('off')  # Hide axis

# Create legend in that subplot
handles, labels = axes[0].get_legend_handles_labels()
legend_ax.legend(handles, labels, loc='center', fontsize=15, frameon=False, ncol=1)

plt.tight_layout()
plt.show()


