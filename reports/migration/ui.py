import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ..constants import neighbouring_states
import matplotlib.pyplot as plt

def ui():
    st.title("Neighbour State Migration vs Obesity Rates")
    state = st.selectbox("State", neighbouring_states.keys())
    plot_graph(state)

geojson_file = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
geojson_gpd = gpd.read_file(geojson_file)
obesity = pd.read_csv("data/Obesity.csv")
obesity_total = obesity[obesity["StratificationCategory1"] == "Total"]

migration = pd.read_csv("data/10-22.csv")

obese_adults = obesity_total[(obesity_total["Question"] == 'Percent of adults aged 18 years and older who have obesity')]

def filter_migration(migration_df):
    filtered_records = []
    for index, row in migration_df.iterrows():
        origin = row['From']
        destination = row['To']
        if destination in neighbouring_states.get(origin, []):
            filtered_records.append(row)
    return pd.DataFrame(filtered_records)

migration = migration.dropna()
filtered_migration_df = filter_migration(migration)
aggregated_migration_df = filtered_migration_df.groupby(['To', 'Year']).sum().reset_index()
aggregated_migration_df = aggregated_migration_df.rename(columns={"Unnamed: 0": "Value"})

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
    print(masked_obesity)
    print(masked_migration)

    ax.plot(masked_migration['Year'], masked_migration['Value_normalized'], label='Migration', marker='x')
    ax.plot(masked_obesity['YearStart'], masked_obesity['Data_Value_normalized'], label='Obesity', marker='o')
    ax.set_xlabel('Year')
    ax.set_ylabel('Normalized Rate')
    ax.set_xlim(2010, 2023)
    ax.set_title(f'Neighboring State Migration and Obesity Rates against Time ({state})')
    ax.legend()

    # Display plot in Streamlit
    st.pyplot(fig)