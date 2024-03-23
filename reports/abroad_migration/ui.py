import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ..constants import neighboring_states
import matplotlib.pyplot as plt
from ..neighbor_migration.ui import correlation_table, plot_graph # reusing these functions
from ..neighbor_migration.ui import aggregated_migration_df, obese_adults

def ui():
    st.title("Foreign Migration vs Obesity Rates")
    state = st.selectbox("State", neighboring_states.keys())

    mva = st.checkbox('Display moving average line')
    window_size = st.slider("Moving Average Window", min_value=1, max_value=5)
    plot_graph(aggregated_foreign_migration_df, obese_adults, state, mva, window_size, "Foreign")
    foreign_cc_df = correlation_table(aggregated_foreign_migration_df, obese_adults, window_size, "Foreign", display=True)
    neighbor_cc_df = correlation_table(aggregated_migration_df, obese_adults, window_size, "Neighboring", display=False)

    combined_cc_df = pd.merge(neighbor_cc_df, foreign_cc_df, on="State", suffixes=(' Neighbor', ' Foreign'))
    combined_cc_df = combined_cc_df.dropna()
    st.title("Comparison between Neighboring & Foreign Migration Correlation Coefficients")
    sort_by = st.selectbox("Sort by", ["Neighbor", "Foreign"])
    comparison_df(combined_cc_df, sort_by)


geojson_file = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
geojson_gpd = gpd.read_file(geojson_file)

migration = pd.read_csv("data/10-22-filled.csv")

migration = migration.dropna()
filtered_migration_df = migration[(migration["From"] == "Abroad") & (migration["Type"] =="Estimate")]
aggregated_foreign_migration_df = filtered_migration_df
aggregated_foreign_migration_df["Value"] = pd.to_numeric(aggregated_foreign_migration_df["Value"])

def min_max_normalize(df, column):
    min_val = df[column].min()
    max_val = df[column].max()
    df[column + '_normalized'] = (df[column] - min_val) / (max_val - min_val)
    return df

def comparison_df(combined_cc_df, sort_by):
    combined_cc_df = combined_cc_df.sort_values("Correlation Coefficient " + sort_by, ascending=False)
    st.dataframe(combined_cc_df)

# def display_bar_charts(df):
#     st.title("Comparison between Neighboring & Foreign Migration Correlation Coefficients")
#     st.write("This display calculates the correlation coefficient of migration rates and obesity rates, \
#              for a given MVA window size and migration type.")
#     st.write("You can hover over the charts to see the exact correlation coefficient value.")
#     df.apply(lambda x: display_bar_chart(x), axis=1)

# def display_bar_chart(row):
#     state = row['State']
#     neighbor_corr = row['Correlation Coefficient Neighbor']
#     foreign_corr = row['Correlation Coefficient Foreign']
    
#     df_row = pd.DataFrame({'Correlation Coefficient': [neighbor_corr, foreign_corr]}, 
#                           index=['Neighbor', 'Foreign'])

#     st.write(f"### {state}")
#     st.bar_chart(df_row, use_container_width=True, height=200, width=200)