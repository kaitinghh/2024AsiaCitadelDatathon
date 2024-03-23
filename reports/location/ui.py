import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from ..constants import neighboring_states

geojson_file = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/us-states.json'
geojson_gpd = gpd.read_file(geojson_file)
obesity = pd.read_csv("data/Obesity.csv")
obesity_total = obesity[obesity["StratificationCategory1"] == "Total"]

migration = pd.read_csv("data/10-22.csv")

def ui():

    st.title('Dynamic Map of Obesity Rates by Region over Time')
    st.write('### Observe how the obesity rates in different states changed over the years from 2011 to 2022.')
    st.write('Black regions are states with missing data.')
    st.write('Disclaimer: Data from before 2011 were filtered from this display as there were a lot of missing data.')

    # years = [2001, 2003, 2005, 2007, 2009, 2011, 2012, 2013, 2014, 
    #          2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]
    year = st.slider('Select a value', min_value=2011, max_value=2022, step=1)

    questions = ['Percent of students in grades 9-12 who have obesity',
       'Percent of students in grades 9-12 who have an overweight classification',
       'Percent of adults aged 18 years and older who have an overweight classification',
       'Percent of adults aged 18 years and older who have obesity']
    question = st.selectbox("Select a question", questions)

    generate_obesity_map(obesity_total, year, question)

    with open(f"reports/location/maps/{year}{question}.html", 'r') as f:
        html_map = f.read()

    components.html(html_map, width=800, height=600)


def generate_obesity_map(df, year, question):
  masked_df = df[(df["YearStart"] == year) & (df["Question"] == question)]

  m = folium.Map(location=[47.751076, -120.740135], zoom_start=3.3)

  folium.Choropleth(
      geo_data=geojson_gpd,
      name='choropleth',
      data=masked_df,
      columns=['LocationDesc', 'Data_Value'],
      key_on='feature.properties.name',
      fill_color='YlGnBu',
      fill_opacity=0.9,
      line_opacity=0.2,
      legend_name='Value',
      bins=[0, 10, 20, 30, 40, 50, 60],
      highlight=True,
  ).add_to(m)
