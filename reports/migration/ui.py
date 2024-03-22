import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ..constants import neighbouring_states
import matplotlib.pyplot as plt

def ui():
    st.title("Neighbour State Migration vs Obesity Rates")
    plot_graph("New York")



geojson_file = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
geojson_gpd = gpd.read_file(geojson_file)
obesity = pd.read_csv("data/Obesity.csv")
obesity_total = obesity[obesity["StratificationCategory1"] == "Total"]

#migrated in 2021, effect will appear in 2022
migration = pd.read_csv("data/21-22.csv")

obese_adults = obesity_total[(obesity_total["Question"] == 'Percent of adults aged 18 years and older who have obesity')]

def filter_migration(migration_df):
    filtered_records = []
    for index, row in migration_df.iterrows():
        origin = row['From']
        destination = row['To']
        if destination in neighbouring_states.get(origin, []):
            filtered_records.append(row)
    return pd.DataFrame(filtered_records)

filtered_migration_df = filter_migration(migration)
aggregated_migration_df = filtered_migration_df.groupby(['To', 'Year']).sum().reset_index()

def min_max_normalize(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    df[column + '_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df

aggregated_migration_df = min_max_normalize(aggregated_migration_df, "Value")
obese_adults = min_max_normalize(obese_adults, "Data_Value")

def plot_graph(state):
    fig, ax = plt.subplots()
    masked_migration = aggregated_migration_df[aggregated_migration_df["To"] == state]
    masked_obesity = obese_adults[obese_adults["LocationDesc"] == state]
    masked_migration["Year"] = pd.to_numeric(masked_migration["Year"])
    masked_obesity["YearStart"] = pd.to_numeric(masked_obesity["YearStart"])
    print(masked_obesity)
    print(masked_migration)

    ax.plot(masked_migration['Year'], masked_migration['Value_normalized'], label='Migration')
    ax.plot(masked_obesity['YearStart'], masked_obesity['Data_Value_normalized'], label='Obesity')
    ax.set_xlabel('X-axis label')
    ax.set_ylabel('Y-axis label')
    ax.set_xlim(2010, 2023)
    ax.set_title('Two DataFrames Plot')
    ax.legend()

    # Display plot in Streamlit
    st.pyplot(fig)