import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ..constants import neighboring_states
import matplotlib.pyplot as plt
import numpy as np

def ui():
    st.title("Neighbour State Migration vs Obesity Rates")
    state = st.selectbox("State", neighboring_states.keys())
    mva = st.checkbox('Display moving average line')
    window_size = st.slider("Moving Average Window", min_value=1, max_value=5)
    plot_graph(aggregated_migration_df, obese_adults, state, mva, window_size)
    correlation_table(aggregated_migration_df, obese_adults, window_size)


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
        if destination in neighboring_states.get(origin, []):
            filtered_records.append(row)
    return pd.DataFrame(filtered_records)

migration = migration.dropna()
migration = migration[migration["Type"] == "Estimate"]
filtered_migration_df = filter_migration(migration)
filtered_migration_df["Value"] = pd.to_numeric(filtered_migration_df["Value"])
aggregated_migration_df = filtered_migration_df.groupby(['To', 'Year']).agg({'Value': 'sum'}).reset_index()

def min_max_normalize(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    df[column + '_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df

def plot_graph(migration_df, obesity_df, state, mva, window_size):
    fig, ax = plt.subplots()
    masked_migration = migration_df[migration_df["To"] == state]
    masked_obesity = obesity_df[obesity_df["LocationDesc"] == state]

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
    moving_average = masked_migration['Value_normalized'].rolling(window=window_size).mean()

    if mva:
        ax.plot(masked_migration['Year'], moving_average, label=f'Moving Average (Window Size = {window_size})', color='red')
    fig.set_size_inches(6, 3.7)
    ax.set_xlabel('Year')
    ax.set_ylabel('Normalized Rate')
    ax.set_xlim(2010, 2023)
    ax.set_title(f'Neighboring State Migration and Obesity Rates against Time ({state})')
    ax.legend()
    
    st.pyplot(fig)

def calc_mva_coefficient(migration_df, obesity_df, state, window_size):
    masked_migration = migration_df[migration_df["To"] == state]
    masked_obesity = obesity_df[obesity_df["LocationDesc"] == state]

    masked_migration = min_max_normalize(masked_migration, "Value")
    masked_obesity = min_max_normalize(masked_obesity, "Data_Value")

    masked_migration["Year"] = pd.to_datetime(masked_migration["Year"], format="%Y")
    masked_obesity["YearStart"] = pd.to_datetime(masked_obesity["YearStart"], format="%Y")

    masked_migration = masked_migration.sort_values(by='Year')
    masked_obesity = masked_obesity.sort_values(by='YearStart')
    moving_average = masked_migration
    moving_average['Value_normalized'] = masked_migration['Value_normalized'].rolling(window=window_size).mean()

    df = pd.merge(moving_average, masked_obesity, how="inner", left_on="Year", right_on="YearStart")
    
    correlation_coefficient = df['Value_normalized'].corr(df['Data_Value_normalized'])
            
    return correlation_coefficient

def correlation_table(migration_df, obesity_df, window_size):
    correlation_df = pd.DataFrame({'State': [], 'Correlation Coefficient': []})

    for state in neighboring_states.keys():
        coefficient = calc_mva_coefficient(migration_df, obesity_df, state, window_size)
        entry = {"State": state, "Correlation Coefficient": coefficient}
        correlation_df = correlation_df.append(entry, ignore_index=True)
    
    correlation_df = correlation_df.sort_values("Correlation Coefficient", ascending=False)

    st.title(f"Correlation Coefficient between Obesity Rate and MVA Neighbor Migration Rates (Window size: {window_size})")
    st.dataframe(correlation_df)
    st.write("Number of states with correlation coefficient > 0.5:", len(correlation_df[correlation_df["Correlation Coefficient"] > 0.5]))
