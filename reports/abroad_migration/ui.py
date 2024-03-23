import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ..constants import neighboring_states
import matplotlib.pyplot as plt

def ui():
    st.title("Neighbour State Migration vs Obesity Rates")
    state = st.selectbox("State", neighboring_states.keys())
    plot_graph(state)

geojson_file = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
geojson_gpd = gpd.read_file(geojson_file)
obesity = pd.read_csv("data/Obesity.csv")
obesity_total = obesity[obesity["StratificationCategory1"] == "Total"]

migration = pd.read_csv("data/10-22.csv")

obese_adults = obesity_total[(obesity_total["Question"] == 'Percent of adults aged 18 years and older who have obesity')]

migration = migration.dropna()
filtered_migration_df = migration[(migration["From"] == "Abroad") & (migration["Type"] =="Estimate")]
aggregated_migration_df = filtered_migration_df
aggregated_migration_df["Value"] = pd.to_numeric(aggregated_migration_df["Value"])

def min_max_normalize(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    df[column + '_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df

def plot_graph(state):
    fig, ax = plt.subplots()
    masked_migration = aggregated_migration_df[aggregated_migration_df["To"] == state]
    masked_obesity = obese_adults[obese_adults["LocationDesc"] == state]

    masked_migration = min_max_normalize(masked_migration, "Value")
    masked_obesity = min_max_normalize(masked_obesity, "Data_Value")

    masked_migration["Year"] = pd.to_numeric(masked_migration["Year"])
    masked_obesity["YearStart"] = pd.to_numeric(masked_obesity["YearStart"])

    masked_migration = masked_migration.sort_values(by='Year')
    masked_obesity = masked_obesity.sort_values(by='YearStart')

    ax.plot(masked_migration['Year'], masked_migration['Value_normalized'], label='Migration', marker='x')
    ax.plot(masked_obesity['YearStart'], masked_obesity['Data_Value_normalized'], label='Obesity', marker='o')
    fig.set_size_inches(6, 3.7)
    ax.set_xlabel('Year')
    ax.set_ylabel('Normalized Rate')
    ax.set_xlim(2010, 2023)
    ax.set_title(f'Foreign Migration and Obesity Rates against Time ({state})')
    ax.legend()

    # Display plot in Streamlit
    st.pyplot(fig)