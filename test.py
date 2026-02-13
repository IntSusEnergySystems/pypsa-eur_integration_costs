#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 28 14:10:16 2026

@author: umair
"""

import pypsa

variable_2030 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/reference/networks/base_s_6___2030.nc")
variable_2040 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/reference/networks/base_s_6___2040.nc")
variable_2050 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/reference/networks/base_s_6___2050.nc")

dispatch_solar_2030 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_solar/networks/base_s_6___2030.nc")
dispatch_solar_2040 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_solar/networks/base_s_6___2040.nc")
dispatch_solar_2050 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_solar/networks/base_s_6___2050.nc")

dispatch_onwind_2030 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_onwind/networks/base_s_6___2030.nc")
dispatch_onwind_2040 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_onwind/networks/base_s_6___2040.nc")
dispatch_onwind_2050 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_onwind/networks/base_s_6___2050.nc")

dispatch_offwind_2030 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_offshore/networks/base_s_6___2030.nc")
dispatch_offwind_2040 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_offshore/networks/base_s_6___2040.nc")
dispatch_offwind_2050 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_offshore/networks/base_s_6___2050.nc")

dispatch_vre_2030 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_vre/networks/base_s_6___2030.nc")
dispatch_vre_2040 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_vre/networks/base_s_6___2040.nc")
dispatch_vre_2050 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_vre/networks/base_s_6___2050.nc")

dispatch_nuclear_2030 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_nuclear/networks/base_s_6___2030.nc")
dispatch_nuclear_2040 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_nuclear/networks/base_s_6___2040.nc")
dispatch_nuclear_2050 = pypsa.Network("/home/umair/PyPSA-Integration_costs/results/flexible_nuclear/networks/base_s_6___2050.nc")


#%%

technologies_solar = ["onwind"]
mask_solar = variable_2030.generators.carrier.isin(technologies_solar)
v_2030 = variable_2030.generators.p_nom_opt.loc[mask_solar].sum()/1e3
v_2040 = variable_2040.generators.p_nom_opt.loc[mask_solar].sum()/1e3
v_2050 = variable_2050.generators.p_nom_opt.loc[mask_solar].sum()/1e3

solar_2030 =dispatch_solar_2030.generators.p_nom_opt.loc[mask_solar].sum()/1e3
solar_2040 = dispatch_solar_2040.generators.p_nom_opt.loc[mask_solar].sum()/1e3
solar_2050 = dispatch_solar_2050.generators.p_nom_opt.loc[mask_solar].sum()/1e3

onwind_2030 =dispatch_onwind_2030.generators.p_nom_opt.loc[mask_solar].sum()/1e3
onwind_2040 =dispatch_onwind_2040.generators.p_nom_opt.loc[mask_solar].sum()/1e3
onwind_2050 =dispatch_onwind_2050.generators.p_nom_opt.loc[mask_solar].sum()/1e3

offwind_2030 =dispatch_offwind_2030.generators.p_nom_opt.loc[mask_solar].sum()/1e3
offwind_2040 =dispatch_offwind_2040.generators.p_nom_opt.loc[mask_solar].sum()/1e3
offwind_2050 =dispatch_offwind_2050.generators.p_nom_opt.loc[mask_solar].sum()/1e3

vre_2030 =dispatch_vre_2030.generators.p_nom_opt.loc[mask_solar].sum()/1e3
vre_2040 =dispatch_vre_2040.generators.p_nom_opt.loc[mask_solar].sum()/1e3
vre_2050 =dispatch_vre_2050.generators.p_nom_opt.loc[mask_solar].sum()/1e3

nuclear_2030 =dispatch_nuclear_2030.generators.p_nom_opt.loc[mask_solar].sum()/1e3
nuclear_2040 =dispatch_nuclear_2040.generators.p_nom_opt.loc[mask_solar].sum()/1e3
nuclear_2050 =dispatch_nuclear_2050.generators.p_nom_opt.loc[mask_solar].sum()/1e3


#%%

technologies_solar = ["nuclear"]
v_2030 = variable_2030.generators_t.p.loc[:, variable_2030.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
v_2040 = variable_2040.generators_t.p.loc[:, variable_2040.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
v_2050 = variable_2050.generators_t.p.loc[:, variable_2050.generators.carrier.isin(technologies_solar)].sum().sum()/1e9

solar_2030 =dispatch_solar_2030.generators_t.p.loc[:, dispatch_solar_2030.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
solar_2040 =dispatch_solar_2040.generators_t.p.loc[:, dispatch_solar_2040.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
solar_2050 = dispatch_solar_2050.generators_t.p.loc[:, dispatch_solar_2050.generators.carrier.isin(technologies_solar)].sum().sum()/1e9

onwind_2030 = dispatch_onwind_2030.generators_t.p.loc[:, dispatch_onwind_2030.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
onwind_2040 = dispatch_onwind_2040.generators_t.p.loc[:, dispatch_onwind_2040.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
onwind_2050 = dispatch_onwind_2050.generators_t.p.loc[:, dispatch_onwind_2050.generators.carrier.isin(technologies_solar)].sum().sum()/1e9

offwind_2030 = dispatch_offwind_2030.generators_t.p.loc[:, dispatch_offwind_2030.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
offwind_2040 = dispatch_offwind_2040.generators_t.p.loc[:, dispatch_offwind_2040.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
offwind_2050 = dispatch_offwind_2050.generators_t.p.loc[:, dispatch_offwind_2050.generators.carrier.isin(technologies_solar)].sum().sum()/1e9

vre_2030 = dispatch_vre_2030.generators_t.p.loc[:, dispatch_vre_2030.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
vre_2040 = dispatch_vre_2040.generators_t.p.loc[:, dispatch_vre_2040.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
vre_2050= dispatch_vre_2050.generators_t.p.loc[:, dispatch_vre_2050.generators.carrier.isin(technologies_solar)].sum().sum()/1e9

nuclear_2030 = dispatch_nuclear_2030.generators_t.p.loc[:, dispatch_nuclear_2030.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
nuclear_2040 = dispatch_nuclear_2040.generators_t.p.loc[:, dispatch_nuclear_2040.generators.carrier.isin(technologies_solar)].sum().sum()/1e9
nuclear_2050 = dispatch_nuclear_2050.generators_t.p.loc[:, dispatch_nuclear_2050.generators.carrier.isin(technologies_solar)].sum().sum()/1e9