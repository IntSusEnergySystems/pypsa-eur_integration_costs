#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import os
import shutil
from datetime import datetime
import plotly.express as px
from jinja2 import Template
import yaml
from scripts.plot_summary import rename_techs, preferred_order
from scripts.make_summary import assign_locations
from scripts.make_summary import assign_carriers
import pypsa
from functools import lru_cache

paths = {
    "variable": "results/reference/networks/base_s_6___{year}.nc",
    "solar": "results/flexible_solar/networks/base_s_6___{year}.nc",
    "onwind": "results/flexible_onwind/networks/base_s_6___{year}.nc",
    "offwind": "results/flexible_offshore/networks/base_s_6___{year}.nc",
    "vre": "results/flexible_vre/networks/base_s_6___{year}.nc",
    "nuclear": "results/flexible_nuclear/networks/base_s_6___{year}.nc",
}

@lru_cache(maxsize=None)
def load_networks(year):
    year = int(year)
    return {
        scen: pypsa.Network(path.format(year=year))
        for scen, path in paths.items()
    }

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
    
def scenario_costs(country):
    costs = [
    ("reference", f"results/reference/country_csvs/{country}_costs.csv"),
    ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_costs.csv"),
    ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_costs.csv"),
    ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_costs.csv"),
    ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_costs.csv"),
    ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_costs.csv"),]
    
    total_costs = {}

    # Process each sensitivity analysis
    for name, file_path in costs:
      # Read the CSV file
      df = pd.read_csv(file_path)
      df = df[['tech', '2030', '2040', '2050']]
      df['Total'] = df[['2030', '2040', '2050']].sum(axis=1)
      df = df[['tech', 'Total']]
      df['Total'] = df['Total'] / 3
      df = df.rename(columns={'Total': name})
      # Store the processed dataframe in the dictionary
      total_costs[name] = df
    
    combined_df = list(total_costs.values())[0]
    for df in list(total_costs.values())[1:]:
     combined_df = pd.merge(combined_df, df, on='tech', how='outer')
     combined_df = combined_df.fillna(0)
     combined_df = combined_df.set_index('tech')
    
    unit='Euros/year'
    if country == "EU":
     title_country = "5 Countries"
    else:
     title_country = country
    title=f'Average Costs Per Year Comparison For {title_country}'
    tech_colors = snakemake.params.plotting["tech_colors"]
    
    fig = go.Figure()
    df_transposed = combined_df.T

    for tech in df_transposed.columns:
      y = df_transposed[tech]
      color = tech_colors.get(tech, 'lightgrey')
      fig.add_trace(go.Bar(
        x=df_transposed.index,
        y=y.where(y > 0, 0),
        name=tech,
        marker_color=color
    ))
      fig.add_trace(go.Bar(
        x=df_transposed.index,
        y=y.where(y < 0, 0),
        name=tech,
        marker_color=color,
        showlegend=False
    ))
    layout_common = dict(
    title=title,
    barmode='relative',  # Changed from 'stack'
    yaxis=dict(title=unit, title_font=dict(size=15), tickfont=dict(size=15)),
    xaxis=dict(tickfont=dict(size=15)),
    legend=dict(font=dict(size=15)),
    hovermode='y'
)
    fig.update_layout(height=1000, width=1000,**layout_common)
    fig.update_layout(hovermode='y')
    
    return fig

def scenario_investment_costs(country):
    costs = [
    ("reference", f"results/reference/country_csvs/{country}_investment costs.csv"),
    ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_investment costs.csv"),
    ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_investment costs.csv"),
    ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_investment costs.csv"),
    ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_investment costs.csv"),
    ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_investment costs.csv"),]
    
    investment_costs = {}
    
    for name, file_path in costs:
      # Read the CSV file
      df = pd.read_csv(file_path)
      df = df[['tech', '2030', '2040', '2050']]
      df['Total'] = df[['2030', '2040', '2050']].sum(axis=1)
      df = df[['tech', 'Total']]
      df['Total'] = df['Total'] / 3
      df = df.rename(columns={'Total': name})
      # Store the processed dataframe in the dictionary
      investment_costs[name] = df
    
    combined_df = list(investment_costs.values())[0]
    for df in list(investment_costs.values())[1:]:
     combined_df = pd.merge(combined_df, df, on='tech', how='outer')
     combined_df = combined_df.fillna(0)
     combined_df = combined_df.set_index('tech')
    
    unit='Euros/year'
    if country == "EU":
     title_country = "5 Countries"
    else:
     title_country = country
    title=f'Average Investment Costs Per Year Comparison For {title_country}'
    tech_colors = snakemake.params.plotting["tech_colors"]
    
    fig = go.Figure()
    df_transposed = combined_df.T

    for tech in df_transposed.columns:
        fig.add_trace(go.Bar(x=df_transposed.index, y=df_transposed[tech], name=tech, marker_color=tech_colors.get(tech, 'lightgrey')))
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', name='Euro reference value = 2020', marker=dict(color='rgba(0,0,0,0)')))
    # Configure layout and labels
    layout_common = dict(
    title=title,
    barmode='relative',  # Changed from 'stack'
    yaxis=dict(title=unit, title_font=dict(size=15), tickfont=dict(size=15)),
    xaxis=dict(tickfont=dict(size=15)),
    legend=dict(font=dict(size=15)),
    hovermode='y'
)
    fig.update_layout(height=1000, width=1000,**layout_common)
    fig.update_layout(hovermode='y')
    
    return fig
    

#%%
def scenario_capacities(country):
    capacities = [
    ("reference", f"results/reference/country_csvs/{country}_capacities.csv"),
    ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_capacities.csv"),
    ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_capacities.csv"),
    ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_capacities.csv"),
    ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_capacities.csv"),
    ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_capacities.csv"),]
    
    groups = [
        ["solar"],
        ["onshore wind", "offshore wind"],
        ["power-to-heat"],
        ["power-to-gas"],
        ["transmission lines"],
        ["power-to-liquid"],
        ["CCGT"],
        ["CHP"],
    ]
    
    groupss = [
        ["solar"],
        ["onshore wind", "offshore wind"],
        ["power-to-heat"],
        ["power-to-gas"],
        ["transmission lines"],
        ["power-to-liquid"],
        ["CCGT"],
        ["nuclear"],
    ]

    value = groups if country != "EU" else groupss

    years = ["2030", "2040", "2050"]
    unit = "[GW]"
    tech_colors = snakemake.params.plotting["tech_colors"]

    # --- Read scenario data ---
    scenario_data = {}
    for scenario, path in capacities:
        df = pd.read_csv(path)
        df = df.set_index("tech")[years]
        scenario_data[scenario] = df

    # --- Create subplot grid ---
    fig = make_subplots(
        rows=len(value),
        cols=3,
        subplot_titles=years,
        shared_yaxes="rows",
        vertical_spacing=0.04,
        horizontal_spacing=0.04
    )

    # --- Plot ---
    for row_idx, tech_group in enumerate(value, start=1):
        for col_idx, year in enumerate(years, start=1):
            for scenario, df in scenario_data.items():
                for tech in tech_group:
                    if tech not in df.index:
                        continue

                    fig.add_trace(
                        go.Bar(
                            x=[scenario],
                            y=[df.loc[tech, year] / 1000],  # MW → GW
                            name=tech,
                            marker_color=tech_colors.get(tech, "grey"),
                            showlegend=(row_idx == 1)
                        ),
                        row=row_idx,
                        col=col_idx
                    )

        # Label each row (group name)
        fig.update_yaxes(
            title_text=", ".join(tech_group),
            row=row_idx,
            col=1
        )

    # --- Layout ---
    fig.update_layout(
        barmode="stack",
        height=250 * len(value),
        width=1600,
        title="Installed Capacities",
        legend_title="Technology"
    )
    fig.update_layout(showlegend=False)
    fig.add_annotation(
    text=unit,
    x=-0.07,
    y=0.5,
    xref="paper",
    yref="paper",
    showarrow=False,
    textangle=-90,
    font=dict(size=14)
)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(tickangle=45)

    return fig

def storage_capacities(country):
    capacities = [
        ("reference", f"results/reference/country_csvs/{country}_storage_capacities.csv"),
        ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_storage_capacities.csv"),
        ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_storage_capacities.csv"),
        ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_storage_capacities.csv"),
        ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_storage_capacities.csv"),
        ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_storage_capacities.csv"),
    ]

    groups = [
        ["Grid-scale battery"],
        ["Thermal Energy Storage"],
        ["Gas storage"]
    ]

    value = groups

    years = ["2030", "2040", "2050"]
    unit = "[GWh]"
    tech_colors = snakemake.params.plotting["tech_colors"]

    # --- Read scenario data ---
    scenario_data = {}
    for scenario, path in capacities:
        df = pd.read_csv(path)
        df = df.set_index("tech")[years]
        scenario_data[scenario] = df

    # --- Create subplot grid ---
    fig = make_subplots(
        rows=len(value),
        cols=3,
        subplot_titles=years,
        shared_yaxes="rows",
        vertical_spacing=0.04,
        horizontal_spacing=0.04
    )

    # --- Plot ---
    for row_idx, tech_group in enumerate(value, start=1):
        for col_idx, year in enumerate(years, start=1):
            for scenario, df in scenario_data.items():
                for tech in tech_group:
                    if tech not in df.index:
                        continue

                    fig.add_trace(
                        go.Bar(
                            x=[scenario],
                            y=[df.loc[tech, year] / 1000],  # MW → GW
                            name=tech,
                            marker_color=tech_colors.get(tech, "grey"),
                            showlegend=(row_idx == 1)
                        ),
                        row=row_idx,
                        col=col_idx
                    )

        # Label each row (group name)
        fig.update_yaxes(
            title_text=", ".join(tech_group),
            row=row_idx,
            col=1
        )

    # --- Layout ---
    fig.update_layout(
        barmode="stack",
        height=300 * len(value),
        width=1200,
        title="Installed Capacities",
        legend_title="Technology"
    )
    fig.update_layout(showlegend=False)
    fig.add_annotation(
    text=unit,
    x=-0.07,
    y=0.5,
    xref="paper",
    yref="paper",
    showarrow=False,
    textangle=-90,
    font=dict(size=14)
)
    fig.update_xaxes(tickangle=45)

    return fig

def integration_costs(country):
    costs = [
    ("reference", f"results/reference/country_csvs/{country}_costs.csv"),
    ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_costs.csv"),
    ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_costs.csv"),
    ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_costs.csv"),
    ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_costs.csv"),
    ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_costs.csv"),]
    
    total_costs = {}
    years = [2030, 2040, 2050]
    # Process each sensitivity analysis
    for name, file_path in costs:
      # Read the CSV file
      df = pd.read_csv(file_path)
      df = df[['tech', '2030', '2040', '2050']]
      total_costs[name] = df.set_index("tech").sum()
      
    costs_variable = total_costs["reference"]
    costs_dispatch = {
    "solar": total_costs["flexible_solar"],
    "onwind": total_costs["flexible_onwind"],
    "offwind": total_costs["flexible_offshore"],
    "vre": total_costs["flexible_vre"],
    "nuclear": total_costs["flexible_nuclear"],
}
    diff = {tech: costs_variable - costs_dispatch[tech] for tech in costs_dispatch}
    
    networks = {y: load_networks(y) for y in years}
    
    carrier_map = {
    "solar": ["solar", "solar rooftop", "solar-hsat"],
    "onwind": ["onwind"],
    "offwind": ["offwind-float", "offwind-ac", "offwind-dc"],
    "vre": ["solar", "solar rooftop", "solar-hsat", "onwind", "offwind-float", "offwind-ac", "offwind-dc"],
    "nuclear": ["nuclear"]
}
    def total_generation(n, carriers, country):
      mask = n.generators.carrier.isin(carriers)
      p = n.generators_t.p.loc[:, mask]

      if country != "EU":
        p = p.loc[:, p.columns.str.contains(country)]

      return p.sum().sum()
    
    gen_variable = {
    tech: {y: total_generation(networks[y]["variable"], carrier_map[tech], country) for y in years}
    for tech in carrier_map
}

    gen_dispatch = {
    tech: {y: total_generation(networks[y][tech], carrier_map[tech], country) for y in years}
    for tech in carrier_map
}
    
    inti = {
    tech: {y: diff[tech][str(y)] / gen_dispatch[tech][y] for y in years}
    for tech in diff}
    
    technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

    tech_colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}

    # If you have inti dict like inti["solar"][2030]
    inti_data = {
    tech: [inti[tech][int(y)] for y in years]
    for tech in technologies
}
    
    # create subplot grid (2 rows, 3 cols)
    fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=[f"{tech.upper() if tech=='vre' else tech.capitalize()} Integration Costs"
                    for tech in technologies]
)

    for i, tech in enumerate(technologies):
     row = i // 3 + 1
     col = i % 3 + 1

     fig.add_trace(
        go.Bar(
            x=years,
            y=inti_data[tech],
            marker_color=tech_colors[tech],
            showlegend=False
        ),
        row=row, col=col
    )

    # Layout formatting
    fig.update_layout(
    height=800,
    width=1200,
    template="plotly_white",
)

    # Y-axis formatting + range
    fig.update_yaxes(title_text="Integration Costs [Eur/MWh]", range=[-20, 120])

    # Make gridlines visible
    fig.update_yaxes(showgrid=True, gridwidth=0.7, gridcolor="lightgray")

    return fig,inti_data

def penetration_level(country):
    costs = [
    ("reference", f"results/reference/country_csvs/{country}_costs.csv"),
    ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_costs.csv"),
    ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_costs.csv"),
    ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_costs.csv"),
    ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_costs.csv"),
    ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_costs.csv"),]
    
    total_costs = {}
    years = [2030, 2040, 2050]
    # Process each sensitivity analysis
    for name, file_path in costs:
      # Read the CSV file
      df = pd.read_csv(file_path)
      df = df[['tech', '2030', '2040', '2050']]
      total_costs[name] = df.set_index("tech").sum()
      
    costs_variable = total_costs["reference"]
    costs_dispatch = {
    "solar": total_costs["flexible_solar"],
    "onwind": total_costs["flexible_onwind"],
    "offwind": total_costs["flexible_offshore"],
    "vre": total_costs["flexible_vre"],
    "nuclear": total_costs["flexible_nuclear"],
}
    diff = {tech: costs_variable - costs_dispatch[tech] for tech in costs_dispatch}
    
    networks = {y: load_networks(y) for y in years}
    
    carrier_map = {
    "solar": ["solar", "solar rooftop", "solar-hsat"],
    "onwind": ["onwind"],
    "offwind": ["offwind-float", "offwind-ac", "offwind-dc"],
    "vre": ["solar", "solar rooftop", "solar-hsat", "onwind", "offwind-float", "offwind-ac", "offwind-dc"],
    "nuclear": ["nuclear"]
}
    def total_generation(n, carriers, country):
      mask = n.generators.carrier.isin(carriers)
      p = n.generators_t.p.loc[:, mask]

      if country != "EU":
        p = p.loc[:, p.columns.str.contains(country)]

      return p.sum().sum()

    gen_dispatch = {
    tech: {y: total_generation(networks[y][tech], carrier_map[tech], country) for y in years}
    for tech in carrier_map
}
    
    inti = {
    tech: {y: diff[tech][str(y)] / gen_dispatch[tech][y] for y in years}
    for tech in diff}
    
    technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

    tech_colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}

    # If you have inti dict like inti["solar"][2030]
    inti_data = {
    tech: [inti[tech][int(y)] for y in years]
    for tech in technologies
}
    scenarios = ["flexible_solar", "flexible_onwind", 
                 "flexible_offshore", "flexible_vre", "flexible_nuclear"]
    scenario_to_tech = {
    "flexible_solar": "solar",
    "flexible_onwind": "onwind",
    "flexible_offshore": "offwind",
    "flexible_vre": "vre",
    "flexible_nuclear": "nuclear",}

    percentage_data = {tech: [] for tech in technologies}
    for scenario in scenarios:
      tech = scenario_to_tech[scenario]

      total_generation = pd.read_excel(
        f"results/{scenario}/htmls/ChartData_{country}.xlsx",
        sheet_name="Chart 22",
        index_col=0,
        skiprows=2)

      total_generation = total_generation.sum(axis=1) * 1e6

      for y in years:
        penetration = (
            gen_dispatch[tech][y] / total_generation[y]
        ) * 100

        percentage_data[tech].append(penetration)
    fig = make_subplots(
    rows=1,
    cols=3,
    shared_yaxes=True,
    subplot_titles=[str(y) for y in years])
    
    for tech in technologies:
     for i, year in enumerate(years):

        fig.add_trace(
            go.Scatter(
                x=[percentage_data[tech][i]],
                y=[inti_data[tech][i]],
                mode="markers",
                marker=dict(
                    size=15,
                    color=tech_colors[tech],
                ),
                name=tech.capitalize(),
                showlegend=(i == 0),  # legend only in first subplot
            ),
            row=1,
            col=i + 1,
        )
    
    for i in range(1, 4):
     fig.update_xaxes(
        title_text="Penetration (%)",
        ticksuffix="%",
        showgrid=True,
        gridcolor="lightgray",
        row=1,
        col=i,
    )
     
    for i in range(1, 4):
     fig.update_yaxes(
        showgrid=True,
        gridcolor="lightgray",
        title_text="Integration Cost [EUR/MWh]",
        row=1,
        col=i,
    )
    fig.update_layout(
    template="simple_white",
    width=1200,
    height=500,
    font=dict(size=14),
    legend=dict(
        title="Technology",
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02,
    ),
)
    return fig

def dispatch(country):
    year = 2050
    
    networks = {year: load_networks(year)}
    
    carrier_map = {
    "solar": ["solar", "solar rooftop", "solar-hsat"],
    "onwind": ["onwind"],
    "offwind": ["offwind-float", "offwind-ac", "offwind-dc"],
    "vre": ["solar", "solar rooftop", "solar-hsat", "onwind", "offwind-float", "offwind-ac", "offwind-dc"],
    "nuclear": ["nuclear"]
}
    def generation_timeseries(n, carriers, country):
      mask = n.generators.carrier.isin(carriers)
      p = n.generators_t.p.loc[:, mask]

      if country != "EU":
        p = p.loc[:, p.columns.str.contains(country)]

      return p.sum(axis=1)/1e3
   
    gen_variable = {
    tech: generation_timeseries(networks[year]["variable"], carrier_map[tech], country)
    for tech in carrier_map
}

    gen_dispatch = {
    tech: generation_timeseries(networks[year][tech], carrier_map[tech], country)
    for tech in carrier_map
}

    tech_colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "vre": "#baf238",
    "nuclear": "#ff8c00"
}
    def slice_series(series, start, end):
     return series.loc[start:end]
    
    fig = make_subplots(
    rows=10,
    cols=3,
    vertical_spacing=0.04,
    horizontal_spacing=0.06,
    subplot_titles = [
    "Solar (2050)", "", "",  
    "Winter week", "Summer week","",
    "Onwind (2050)", "", "",  
    "Winter week", "Summer week","",
    "Offwind (2050)", "", "",  
    "Winter week", "Summer week","",
    "VRE (2050)", "", "",  
    "Winter week", "Summer week","",
    "Nuclear (2050)", "", "",  
    "Winter week", "Summer week","",
]
)
    tech_positions = {
    "solar": 0,
    "onwind": 2,
    "offwind": 4,
    "vre": 6,
    "nuclear": 8,
}
    start_winter = pd.to_datetime('2013-01-01 00:00:00')
    end_winter = pd.to_datetime('2013-01-07 23:00:00')

    start_summer = pd.to_datetime('2013-07-01 00:00:00')
    end_summer = pd.to_datetime('2013-07-07 23:00:00')
    for tech, base_row in tech_positions.items():
      variable = gen_variable[tech]
      dispatch = gen_dispatch[tech]

      fig.add_trace(
        go.Scatter(
            x=variable.index,
            y=variable,
            line=dict(color=tech_colors[tech]),
            name=f"{tech} variable",
            showlegend=True,
        ),
        row=base_row + 1,
        col=1,
    )

      fig.add_trace(
        go.Scatter(
            x=dispatch.index,
            y=dispatch,
            line=dict(color="black", width=1),
            name=f"{tech} flexible",
            showlegend=True,
        ),
        row=base_row + 1,
        col=1,
    )

    # WINTER
      fig.add_trace(
        go.Scatter(
            x=slice_series(variable, start_winter, end_winter).index,
            y=slice_series(variable, start_winter, end_winter),
            line=dict(color=tech_colors[tech]),
            showlegend=False,
        ),
        row=base_row + 2,
        col=1,
    )

      fig.add_trace(
        go.Scatter(
            x=slice_series(dispatch, start_winter, end_winter).index,
            y=slice_series(dispatch, start_winter, end_winter),
            line=dict(color="black"),
            showlegend=False,
        ),
        row=base_row + 2,
        col=1,
    )

    # SUMMER
      fig.add_trace(
        go.Scatter(
            x=slice_series(variable, start_summer, end_summer).index,
            y=slice_series(variable, start_summer, end_summer),
            line=dict(color=tech_colors[tech]),
            showlegend=False,
        ),
        row=base_row + 2,
        col=2,
    )

      fig.add_trace(
        go.Scatter(
            x=slice_series(dispatch, start_summer, end_summer).index,
            y=slice_series(dispatch, start_summer, end_summer),
            line=dict(color="black"),
            showlegend=False,
        ),
        row=base_row + 2,
        col=2,
    )
    
    for r in [1, 3, 5,7,9]:
      fig.update_xaxes(
        tickformat="%b",
        row=r,
        col=1,
    )

    # Weekly plots → day of month
    for r in [2,3,5,6,8,9,10]:
     fig.update_xaxes(
        tickformat="%d",
        row=r,
        col=1,
    )
     fig.update_xaxes(
        tickformat="%d",
        row=r,
        col=2,
    )

    fig.update_layout(
    template="simple_white",
    height=1400,
    width=1800,
    font=dict(size=12),
)

    fig.update_yaxes(
    title_text="GW",
    row=1,
    col=1,
)
    return fig

def valcoe(country):
    planning_horizons = [2030, 2040, 2050]
    valcoe_dict = {}   
    lcoe_dict = {}                
    for planning_horizon in planning_horizons:
      n=pypsa.Network(f"results/reference/networks/base_s_6___{planning_horizon}.nc")
      if country == 'EU':
        prices_marginal = n.buses_t.marginal_price.loc[:, n.buses.carrier == "AC"]
        prices_marginal = prices_marginal.sum(axis=0)/8760
        prices_marginal = prices_marginal.sum()/6
        
        wholesale_prices = n.buses_t.marginal_price.loc[:, n.buses.carrier == "AC"]
        wholesale_prices = wholesale_prices.sum(axis=1)/6
        
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
        
        load = n.loads_t.p.loc[:, n.loads.carrier.isin([
            "electricity", 
            "industry electricity", 
            "agriculture electricity", 
            "land transport EV",])].sum(axis=1)
        opt_solar = n.generators.p_nom_opt.filter(like="solar")
        opt_solar = opt_solar.drop([idx for idx in opt_solar.index if "thermal collector" in idx])
        opt_solar = opt_solar.groupby(opt_solar.index).sum().sum()
        opt_offwind = n.generators.p_nom_opt.filter(like="offwind")
        opt_offwind = opt_offwind.groupby(opt_offwind.index).sum().sum()
        opt_onwind = n.generators.p_nom_opt.filter(like="onwind")
        opt_onwind = opt_onwind.groupby(opt_onwind.index).sum().sum()
        opt_nuc = n.generators.p_nom_opt.filter(like="nuclear")
        opt_nuc = opt_nuc.groupby(opt_nuc.index).sum().sum()
      else:
        prices_marginal = n.buses_t.marginal_price.filter(like=country).loc[:, n.buses.carrier == "AC"]
        prices_marginal = prices_marginal.sum(axis=0).sum()/8760
        
        wholesale_prices = n.buses_t.marginal_price.filter(like=country).loc[:, n.buses.carrier == "AC"]
        wholesale_prices = wholesale_prices.sum(axis=1)
        generation_solar = n.generators_t.p.filter(like=country).filter(like="solar")
        generation_solar = generation_solar.drop(columns=[col for col in generation_solar.columns if "thermal collector" in col])
        generation_solar = generation_solar.sum(axis=1)
        generation_solar_tot = generation_solar.sum().sum()

        generation_offwind = n.generators_t.p.filter(like=country).filter(like="offwind")
        generation_offwind = generation_offwind.sum(axis=1)
        generation_offwind_tot = generation_offwind.sum().sum()

        generation_onwind = n.generators_t.p.filter(like=country).filter(like="onwind")
        generation_onwind = generation_onwind.sum(axis=1)
        generation_onwind_tot = generation_onwind.sum().sum()

        generation_nuc = n.generators_t.p.filter(like=country).filter(like="nuclear")
        generation_nuc = generation_nuc.sum(axis=1) if generation_nuc is not None else 0.0
        generation_nuc_tot = generation_nuc.sum().sum() if generation_nuc is not None else 0.0
        
        load = n.loads_t.p.filter(like=country).loc[:, n.loads.carrier.isin([
            "electricity", 
            "industry electricity", 
            "agriculture electricity", 
            "land transport EV",])].sum(axis=1)
        
        opt_solar = n.generators.p_nom_opt.filter(like=country).filter(like="solar")
        opt_solar = opt_solar.drop([idx for idx in opt_solar.index if "thermal collector" in idx])
        opt_solar = opt_solar.groupby(opt_solar.index).sum().sum()
        opt_offwind = n.generators.p_nom_opt.filter(like=country).filter(like="offwind")
        opt_offwind = opt_offwind.groupby(opt_offwind.index).sum().sum()
        opt_onwind = n.generators.p_nom_opt.filter(like=country).filter(like="onwind")
        opt_onwind = opt_onwind.groupby(opt_onwind.index).sum().sum()
        opt_nuc = n.generators.p_nom_opt.filter(like=country).filter(like="nuclear")
        opt_nuc = opt_nuc.groupby(opt_nuc.index).sum().sum() if generation_nuc is not None else 0.0
        
      costs = [
     ("reference", f"results/reference/country_csvs/{country}_costs.csv")]

      total_costs = {}
      # Process each sensitivity analysis
      for name, file_path in costs:
       # Read the CSV file
       df = pd.read_csv(file_path)
       df = df[['tech', '2030', '2040', '2050']]
       total_costs[name] = df.set_index("tech")
       
      year = str(planning_horizon)
      total_costs_year = total_costs["reference"][year]
      solar_costs= total_costs_year["solar"]
      onshore_costs= total_costs_year["onshore wind"]
      offshore_costs= total_costs_year["offshore wind"]
      nuclear_costs  = total_costs_year.get("nuclear", 0.0)
        
      lcoe_value_solar = (solar_costs/ generation_solar_tot)
      lcoe_value_offwind = (offshore_costs/ generation_offwind_tot)
      lcoe_value_onwind = (onshore_costs/ generation_onwind_tot)
      lcoe_value_nuc = (nuclear_costs/ generation_nuc_tot)

      lcoe_dict[planning_horizon] = {
         "solar": lcoe_value_solar,
         "onwind": lcoe_value_onwind,
         "offwind": lcoe_value_offwind,
         "nuclear": lcoe_value_nuc
     }
      total_generation = pd.read_excel(
        f"results/reference/htmls/ChartData_{country}.xlsx",
        sheet_name="Chart 22",
        index_col=0,
        skiprows=2)

      total_generation = total_generation.sum(axis=1) * 1e6
      total_generation = total_generation[planning_horizon]
      energy_val_tot = (wholesale_prices * total_generation) / (total_generation)
      energy_val_tot = energy_val_tot.fillna(0).sum()/8760
      energy_val_solar = (wholesale_prices * generation_solar) / (generation_solar)
      energy_val_solar = energy_val_solar.fillna(0).sum()/8760
      energy_val_onwind = (wholesale_prices * generation_onwind) / (generation_onwind)
      energy_val_onwind = energy_val_onwind.fillna(0).sum()/8760
      energy_val_offwind = (wholesale_prices * generation_offwind) / (generation_offwind)
      energy_val_offwind = energy_val_offwind.fillna(0).sum()/8760
      energy_val_nuc = (wholesale_prices * generation_nuc) / (generation_nuc)
      energy_val_nuc = energy_val_nuc.fillna(0).sum()/8760 if generation_nuc is not None else 0.0
      peak_demand = load.dropna().nlargest(30)
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
      capacity_factor_nuc = generation_nuc_tot / (opt_nuc * 8760) if generation_nuc is not None else 0.0
      capacity_value_solar = (capacity_credit_solar * basic_capacity_value) / (capacity_factor_solar * (8760/1000))
      capacity_value_onwind = (capacity_credit_onwind * basic_capacity_value) / (capacity_factor_onwind * (8760/1000))
      capacity_value_offwind = (capacity_credit_offwind * basic_capacity_value) / (capacity_factor_offwind * (8760/1000))
      capacity_value_nuc = (capacity_credit_nuc * basic_capacity_value) / (capacity_factor_nuc * (8760/1000)) if generation_nuc is not None else 0.0
      capacity_value_tot = (1* basic_capacity_value) / (1 * (8760/1000))

      flexibility_value_mul_solar =  (generation_solar / total_generation).sum()/8760
      flexibility_value_solar = (flexibility_value_mul_solar * basic_capacity_value) / (capacity_factor_solar * (8760/1000))
      flexibility_value_mul_onwind =  (generation_onwind / total_generation).sum()/8760
      flexibility_value_onwind = (flexibility_value_mul_onwind * basic_capacity_value) / (capacity_factor_onwind * (8760/1000))
      flexibility_value_mul_offwind =  (generation_offwind / total_generation).sum()/8760
      flexibility_value_offwind = (flexibility_value_mul_offwind * basic_capacity_value) / (capacity_factor_offwind * (8760/1000))
      flexibility_value_mul_nuc =  (generation_nuc / total_generation).sum()/8760 if generation_nuc is not None else 0.0
      flexibility_value_nuc = (flexibility_value_mul_nuc * basic_capacity_value) / (capacity_factor_nuc * (8760/1000)) if generation_nuc is not None else 0.0
      flexibility_value_tot = (1 * basic_capacity_value) / (1 * (8760/1000)) if generation_nuc is not None else 0.0

      valcoe_solar = lcoe_value_solar + (energy_val_tot - energy_val_solar) + (capacity_value_tot - capacity_value_solar) + (flexibility_value_tot - flexibility_value_solar)
      valcoe_onwind = lcoe_value_onwind + (energy_val_tot - energy_val_onwind) + (capacity_value_tot - capacity_value_onwind) + (flexibility_value_tot - flexibility_value_onwind)
      valcoe_offwind = lcoe_value_offwind + (energy_val_tot - energy_val_offwind) + (capacity_value_tot - capacity_value_offwind) + (flexibility_value_tot - flexibility_value_offwind)
      valcoe_nuc = lcoe_value_nuc + (energy_val_tot - energy_val_nuc) + (capacity_value_tot - capacity_value_nuc) + (flexibility_value_tot - flexibility_value_nuc)
      valcoe_nuc = 0 if opt_nuc < 1 else valcoe_nuc
      valcoe_dict[planning_horizon] = {
         "solar": valcoe_solar,
         "onwind": valcoe_onwind,
         "offwind": valcoe_offwind,
         "nuclear": valcoe_nuc
     }
      _, inti_data = integration_costs(country)
    technologies = ["solar", "onwind", "offwind", "nuclear"]
    colors = {
    "solar": "#f9d002",
    "onwind": "#235ebc",
    "offwind": "#6895dd",
    "nuclear": "#ff8c00",
} 
    fig = make_subplots(rows=2, cols=2, subplot_titles=[t.capitalize() for t in technologies],shared_yaxes=True)

    for i, tech in enumerate(technologies):
      row = i // 2 + 1
      col = i % 2 + 1

      lcoe_vals = [lcoe_dict[y][tech] for y in planning_horizons]
      valcoe_vals = [valcoe_dict[y][tech] for y in planning_horizons]
      adjusted_lcoe_vals = [lcoe_dict[y][tech] + inti_data[tech][j] for j, y in enumerate(planning_horizons)]

      # Original LCOE
      fig.add_trace(
        go.Bar(
            x=planning_horizons,
            y=lcoe_vals,
            name="LCOE",
            marker=dict(color=colors[tech])
        ),
        row=row,
        col=col
    )

    # Adjusted LCOE with pattern
      fig.add_trace(
        go.Bar(
            x=planning_horizons,
            y=adjusted_lcoe_vals,
            name="Adjusted LCOE",
            marker=dict(color=colors[tech], pattern=dict(shape="/"))
        ),
        row=row,
        col=col
    )

    # VALCOE with a different pattern
      fig.add_trace(
        go.Bar(
            x=planning_horizons,
            y=valcoe_vals,
            name="VALCOE",
            marker=dict(color=colors[tech], pattern=dict(shape="\\"))
        ),
        row=row,
        col=col
    )
    fig.update_layout(
    barmode="group",
    height=800,
    width=1200,
    template="plotly_white",
    yaxis_title="EUR/MWh",
)
    return fig

def total_comparison(country):
    years = [2030, 2040, 2050]
    networks = {y: load_networks(y) for y in years}
    
    carrier_map = {
    "solar": ["solar", "solar rooftop", "solar-hsat"],
    "onwind": ["onwind"],
    "offwind": ["offwind-float", "offwind-ac", "offwind-dc"],
    "vre": ["solar", "solar rooftop", "solar-hsat", "onwind", "offwind-float", "offwind-ac", "offwind-dc"],
    "nuclear": ["nuclear"]
}
    def total_generation(n, carriers, country):
      mask = n.generators.carrier.isin(carriers)
      p = n.generators_t.p.loc[:, mask]

      if country != "EU":
        p = p.loc[:, p.columns.str.contains(country)]

      return p.sum().sum()

    gen_dispatch = {
    tech: {y: total_generation(networks[y][tech], carrier_map[tech], country) for y in years}
    for tech in carrier_map
}

    
    df_variable=pd.read_csv(f"results/reference/country_csvs/{country}_costs.csv")
    filtered_df_variable = df_variable[df_variable['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network'])]
    filtered_df_variable = filtered_df_variable[['2030', '2040', '2050']].sum()

    df_solar=pd.read_csv(f"results/flexible_solar/country_csvs/{country}_costs.csv")
    filtered_df_solar = df_solar[df_solar['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network'])]
    filtered_df_solar = filtered_df_solar[['2030', '2040', '2050']].sum()
    grid_solar = filtered_df_variable - filtered_df_solar
    generation_solar = pd.Series({
    str(y): gen_dispatch['solar'][y] for y in years})

    df_onwind=pd.read_csv(f"results/flexible_onwind/country_csvs/{country}_costs.csv")
    filtered_df_onwind = df_onwind[df_onwind['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network'])]
    filtered_df_onwind = filtered_df_onwind[['2030', '2040', '2050']].sum()
    grid_onwind = filtered_df_variable - filtered_df_onwind
    generation_onwind = pd.Series({
    str(y): gen_dispatch['onwind'][y] for y in years})

    df_offwind=pd.read_csv(f"results/flexible_offshore/country_csvs/{country}_costs.csv")
    filtered_df_offwind = df_offwind[df_offwind['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network'])]
    filtered_df_offwind = filtered_df_offwind[['2030', '2040', '2050']].sum()
    grid_offwind = filtered_df_variable - filtered_df_offwind
    generation_offwind = pd.Series({
    str(y): gen_dispatch['offwind'][y] for y in years})

    df_vre=pd.read_csv(f"results/flexible_vre/country_csvs/{country}_costs.csv")
    filtered_df_vre = df_vre[df_vre['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network'])]
    filtered_df_vre = filtered_df_vre[['2030', '2040', '2050']].sum()
    grid_vre = filtered_df_variable - filtered_df_vre
    generation_vre = pd.Series({
    str(y): gen_dispatch['vre'][y] for y in years})

    df_nuclear=pd.read_csv(f"results/flexible_nuclear/country_csvs/{country}_costs.csv")
    filtered_df_nuclear = df_nuclear[df_nuclear['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network'])]
    filtered_df_nuclear = filtered_df_nuclear[['2030', '2040', '2050']].sum()
    grid_nuclear = filtered_df_variable - filtered_df_nuclear
    generation_nuclear = pd.Series({
    str(y): gen_dispatch['nuclear'][y] for y in years})

    grid_costs_solar = grid_solar / generation_solar
    grid_costs_onwind = grid_onwind / generation_onwind
    grid_costs_offwind = grid_offwind / generation_offwind
    grid_costs_vre = grid_vre / generation_vre
    grid_costs_nuclear = grid_nuclear / generation_nuclear

    storage_df_variable = df_variable[df_variable['tech'].isin(['BEV charger','TES & H2 storage','battery storage','CCUS'])]
    storage_df_variable = storage_df_variable[['2030', '2040', '2050']].sum()

    storage_df_solar = df_solar[df_solar['tech'].isin(['BEV charger','TES & H2 storage','battery storage','CCUS'])]
    storage_df_solar = storage_df_solar[['2030', '2040', '2050']].sum()
    storage_solar = storage_df_variable - storage_df_solar

    storage_df_onwind = df_onwind[df_onwind['tech'].isin(['BEV charger','TES & H2 storage','battery storage','CCUS'])]
    storage_df_onwind = storage_df_onwind[['2030', '2040', '2050']].sum()
    storage_onwind = storage_df_variable - storage_df_onwind

    storage_df_offwind = df_offwind[df_offwind['tech'].isin(['BEV charger','TES & H2 storage','battery storage','CCUS'])]
    storage_df_offwind = storage_df_offwind[['2030', '2040', '2050']].sum()
    storage_offwind = storage_df_variable - storage_df_offwind

    storage_df_vre = df_vre[df_vre['tech'].isin(['BEV charger','TES & H2 storage','battery storage','CCUS'])]
    storage_df_vre = storage_df_vre[['2030', '2040', '2050']].sum()
    storage_vre = storage_df_variable - storage_df_vre

    storage_df_nuclear = df_nuclear[df_nuclear['tech'].isin(['BEV charger','TES & H2 storage','battery storage','CCUS'])]
    storage_df_nuclear = storage_df_nuclear[['2030', '2040', '2050']].sum()
    storage_nuclear = storage_df_variable - storage_df_nuclear

    storage_costs_solar = storage_solar / generation_solar
    storage_costs_onwind = storage_onwind / generation_onwind
    storage_costs_offwind = storage_offwind / generation_offwind
    storage_costs_vre = storage_vre / generation_vre
    storage_costs_nuclear = storage_nuclear / generation_nuclear

    df_variable = df_variable[~df_variable['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network','BEV charger','TES & H2 storage','battery storage','CCUS'])]
    df_solar = df_solar[~df_solar['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network','BEV charger','TES & H2 storage','battery storage','CCUS'])]
    df_onwind = df_onwind[~df_onwind['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network','BEV charger','TES & H2 storage','battery storage','CCUS'])]
    df_offwind = df_offwind[~df_offwind['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network','BEV charger','TES & H2 storage','battery storage','CCUS'])]
    df_vre = df_vre[~df_vre['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network','BEV charger','TES & H2 storage','battery storage','CCUS'])]
    df_nuclear = df_nuclear[~df_nuclear['tech'].isin(['CO2 pipeline','H2 & gas pipelines','transmission lines','distribution network','BEV charger','TES & H2 storage','battery storage','CCUS'])]

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
    
    costs = [
    ("reference", f"results/reference/country_csvs/{country}_costs.csv"),
    ("flexible_solar", f"results/flexible_solar/country_csvs/{country}_costs.csv"),
    ("flexible_onwind", f"results/flexible_onwind/country_csvs/{country}_costs.csv"),
    ("flexible_offshore", f"results/flexible_offshore/country_csvs/{country}_costs.csv"),
    ("flexible_vre", f"results/flexible_vre/country_csvs/{country}_costs.csv"),
    ("flexible_nuclear", f"results/flexible_nuclear/country_csvs/{country}_costs.csv"),]
    
    total_costs = {}
    # Process each sensitivity analysis
    for name, file_path in costs:
      # Read the CSV file
      df = pd.read_csv(file_path)
      df = df[['tech', '2030', '2040', '2050']]
      total_costs[name] = df.set_index("tech").sum()
      
    costs_variable = total_costs["reference"]
    costs_dispatch = {
    "solar": total_costs["flexible_solar"],
    "onwind": total_costs["flexible_onwind"],
    "offwind": total_costs["flexible_offshore"],
    "vre": total_costs["flexible_vre"],
    "nuclear": total_costs["flexible_nuclear"],
}
    diff = {tech: costs_variable - costs_dispatch[tech] for tech in costs_dispatch}
    
    inti = {
    tech: {y: diff[tech][str(y)] / gen_dispatch[tech][y] for y in years}
    for tech in diff}
    
    technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

    # If you have inti dict like inti["solar"][2030]
    inti_data = {
    tech: [inti[tech][int(y)] for y in years]
    for tech in technologies
}
    lcoe_dict = {} 
    planning_horizons = [2030, 2040, 2050]               
    for planning_horizon in planning_horizons:
      n=pypsa.Network(f"results/reference/networks/base_s_6___{planning_horizon}.nc")
      if country == 'EU':
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
      else:
        generation_solar = n.generators_t.p.filter(like=country).filter(like="solar")
        generation_solar = generation_solar.drop(columns=[col for col in generation_solar.columns if "thermal collector" in col])
        generation_solar = generation_solar.sum(axis=1)
        generation_solar_tot = generation_solar.sum().sum()

        generation_offwind = n.generators_t.p.filter(like=country).filter(like="offwind")
        generation_offwind = generation_offwind.sum(axis=1)
        generation_offwind_tot = generation_offwind.sum().sum()

        generation_onwind = n.generators_t.p.filter(like=country).filter(like="onwind")
        generation_onwind = generation_onwind.sum(axis=1)
        generation_onwind_tot = generation_onwind.sum().sum()

        generation_nuc = n.generators_t.p.filter(like=country).filter(like="nuclear")
        generation_nuc = generation_nuc.sum(axis=1)
        generation_nuc_tot = generation_nuc.sum().sum() if generation_nuc is not None else 0.0
        
      costs = [
     ("reference", f"results/reference/country_csvs/{country}_costs.csv")]

      total_costs = {}
      # Process each sensitivity analysis
      for name, file_path in costs:
       # Read the CSV file
       df = pd.read_csv(file_path)
       df = df[['tech', '2030', '2040', '2050']]
       total_costs[name] = df.set_index("tech")
       
      year = str(planning_horizon)
      total_costs_year = total_costs["reference"][year]
      solar_costs= total_costs_year["solar"]
      onshore_costs= total_costs_year["onshore wind"]
      offshore_costs= total_costs_year["offshore wind"]
      nuclear_costs= total_costs_year.get("nuclear", 0.0)
        
      lcoe_value_solar = (solar_costs/ generation_solar_tot)
      lcoe_value_offwind = (offshore_costs/ generation_offwind_tot)
      lcoe_value_onwind = (onshore_costs/ generation_onwind_tot)
      lcoe_value_vre = (lcoe_value_solar + lcoe_value_offwind + lcoe_value_onwind) /3
      lcoe_value_nuc = (nuclear_costs/ generation_nuc_tot)

      lcoe_dict[planning_horizon] = {
         "solar": lcoe_value_solar,
         "onwind": lcoe_value_onwind,
         "offwind": lcoe_value_offwind,
         "vre": lcoe_value_vre,
         "nuclear": lcoe_value_nuc
     }
    
    years = [2030, 2040, 2050]
    technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

    grid_costs = {
    "solar": grid_costs_solar,
    "onwind": grid_costs_onwind,
    "offwind": grid_costs_offwind,
    "vre": grid_costs_vre,
    "nuclear": grid_costs_nuclear
}

    storage_costs = {
    "solar": storage_costs_solar,
    "onwind": storage_costs_onwind,
    "offwind": storage_costs_offwind,
    "vre": storage_costs_vre,
    "nuclear": storage_costs_nuclear
}

    flex_costs = {
    "solar": flex_costs_solar,
    "onwind": flex_costs_onwind,
    "offwind": flex_costs_offwind,
    "vre": flex_costs_vre,
    "nuclear": flex_costs_nuclear
}
      
    years = [2030, 2040, 2050]
    technologies = ["solar", "onwind", "offwind", "vre", "nuclear"]

    fig = make_subplots(
    rows=len(years),
    cols=len(technologies),
    subplot_titles=[
        f"{tech.capitalize()} – {year}"
        for year in years
        for tech in technologies
    ],
    shared_yaxes=True,
)

    for row, year in enumerate(years, start=1):
     for col, tech in enumerate(technologies, start=1):

        base_lcoe = lcoe_dict[year][tech]
        grid = grid_costs[tech][str(year)]
        storage = storage_costs[tech][str(year)]
        flex = flex_costs[tech][str(year)]
        
        fig.add_trace(
            go.Waterfall(
                orientation="v",
                measure=[
                    "absolute",
                    "relative",
                    "relative",
                    "relative",
                    "total"
                ],
                x=[
                    "LCOE",
                    "Grid Investments",
                    "Storage Investments",
                    "Other Investments",
                    "Adjusted LCOE"
                ],
                y=[
                    base_lcoe,
                    grid,
                    storage,
                    flex,
                    base_lcoe + grid + storage + flex
                ],
                
                connector={"line": {"width": 1, "color": "rgb(63, 63, 63)", "dash": "dot"}},
                showlegend=False,),
            row=row,
            col=col,
        )
        
    fig.update_layout(
    title=f"LCOE decomposition waterfalls – {country}",
    height=300 * len(years),
    template="plotly_white"
)

    fig.update_yaxes(title="€/MWh")
    
    return fig
def create_combined_scenario_chart_country(country, output_folder='results/scenario_results/'):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Create combined HTML
    combined_html = "<html><head><title>Integration Costs Results</title></head><body>"
    
    #load the html plot flags
    with open(snakemake.input.plots_html, 'r') as file:
     plots = yaml.safe_load(file)
    scenario_plots = plots.get("Scenario_plots", {})
    
    # Create bar chart
    if scenario_plots["Annual Costs"] == True:
     bar_chart = scenario_costs(country)
     combined_html += f"<div><h2>{country} - Annual Costs</h2>{bar_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    
    if scenario_plots["Annual Investment Costs"] == True:
     bar_chart_investment = scenario_investment_costs(country)
     combined_html += f"<div><h2>{country} - Annual Investment Costs</h2>{bar_chart_investment.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    
    # Create capacities chart
    if scenario_plots["Capacities"] == True:
     capacities_chart = scenario_capacities(country)
     combined_html += f"<div><h2>{country} - Capacities</h2>{capacities_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    
    # Create storage capacities chart
    if scenario_plots["Storage Capacities"] == True:
     storage_capacities_chart = storage_capacities(country)
     combined_html += f"<div><h2>{country} -  Storage Capacities</h2>{storage_capacities_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    
    if scenario_plots["Integration Costs"] == True:
     fig, _ = integration_costs(country)
     combined_html += f"<div><h2>{country} -  Integration Costs</h2>{fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
     
    if scenario_plots["Penetration Level"] == True:
     penetration_level_chart = penetration_level(country)
     combined_html += f"<div><h2>{country} -  Penetration Level</h2>{penetration_level_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
     
    if scenario_plots["Dispatch"] == True:
     dispatch_chart = dispatch(country)
     combined_html += f"<div><h2>{country} -  Dispatch of Technologies</h2>{dispatch_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
     
    if scenario_plots["Valcoe"] == True:
     valcoe_chart = valcoe(country)
     combined_html += f"<div><h2>{country} -  VALCOE Comparison</h2>{valcoe_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
     
    if scenario_plots["Waterfall"] == True:
     waterfall_chart = total_comparison(country)
     combined_html += f"<div><h2>{country} -  Total Comparison</h2>{waterfall_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
     
    combined_html += "</body></html>"
    table_of_contents_content = ""
    main_content = ''
    # Create the content for the "Table of Contents" and "Main" sections
    if scenario_plots["Annual Costs"] == True:
     table_of_contents_content += f"<a href='#{country} - Annual Costs'>Annual Costs</a><br>"
    if scenario_plots["Annual Investment Costs"] == True:
     table_of_contents_content += f"<a href='#{country} - Annual Investment Costs'>Annual Investment Costs</a><br>"
    if scenario_plots["Capacities"] == True:
     table_of_contents_content += f"<a href='#{country} - Capacities'>Capacities</a><br>"
    if scenario_plots["Storage Capacities"] == True:
     table_of_contents_content += f"<a href='#{country} - Storage Capacities'>Storage Capacities</a><br>"
    if scenario_plots["Integration Costs"] == True:
     table_of_contents_content += f"<a href='#{country} - Integration Costs'>Integration Costs</a><br>"
    if scenario_plots["Penetration Level"] == True:
     table_of_contents_content += f"<a href='#{country} - Penetration Level'>Penetration Level</a><br>"
    if scenario_plots["Dispatch"] == True:
     table_of_contents_content += f"<a href='#{country} - Dispatch of Technologies'>Dispatch of Technologies</a><br>"
    if scenario_plots["Valcoe"] == True:
     table_of_contents_content += f"<a href='#{country} - VALCOE Comparison'>VALCOE Comparison</a><br>"
    if scenario_plots["Waterfall"] == True:
     table_of_contents_content += f"<a href='#{country} - Total Comparison'>VALCOE Comparison</a><br>"
    # Add more links for other plots
    if scenario_plots["Annual Costs"] == True:
     main_content += f"<div id='{country} - Annual Costs'><h2>{country} - Annual Costs</h2>{bar_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Annual Investment Costs"] == True:
     main_content += f"<div id='{country} - Annual Investment Costs'><h2>{country} - Annual Investment Costs</h2>{bar_chart_investment.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Capacities"] == True:
     main_content += f"<div id='{country} - Capacities'><h2>{country} - Capacities</h2>{capacities_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Storage Capacities"] == True:
     main_content += f"<div id='{country} - Storage Capacities'><h2>{country} - Storage Capacities</h2>{storage_capacities_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Integration Costs"] == True:
     main_content += f"<div id='{country} - Integration Costs'><h2>{country} - Integration Costs</h2>{fig.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Penetration Level"] == True:
     main_content += f"<div id='{country} - Penetration Level'><h2>{country} - Penetration Level</h2>{penetration_level_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Dispatch"] == True:
     main_content += f"<div id='{country} - Dispatch of Technologies'><h2>{country} - Dispatch of Technologies</h2>{dispatch_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Valcoe"] == True:
     main_content += f"<div id='{country} - VALCOE Comparison'><h2>{country} - VALCOE Comparison</h2>{valcoe_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    if scenario_plots["Waterfall"] == True:
     main_content += f"<div id='{country} - Total Comparison'><h2>{country} - Total Comparison</h2>{waterfall_chart.to_html(full_html=False, include_plotlyjs='cdn')}</div>"
    template_path =  snakemake.input.template
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
        template = Template(template_content)
        
    rendered_html = template.render(
    title=f"{country} - Combined Plots",
    country=country,
    TABLE_OF_CONTENTS=table_of_contents_content,
    MAIN=main_content,)
    
    combined_file_path = os.path.join(output_folder, f"{country}_combined_scenario_chart.html")
    with open(combined_file_path, "w") as combined_file:
     combined_file.write(rendered_html)




if __name__ == "__main__":
    if "snakemake" not in globals():
        #from _helpers import mock_snakemake

        #snakemake = mock_snakemake("prepare_scenarios")
        import pickle
        with open("snakemake_dump.pkl", "rb") as f:
            snakemake = pickle.load(f)

        
    total_country = 'EU'
    countries = snakemake.params.countries 
    countries.append(total_country) 
    config = snakemake.config
    for country in countries:
        create_combined_scenario_chart_country(country)
        
    
 
