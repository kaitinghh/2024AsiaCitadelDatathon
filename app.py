import streamlit as st
import os
import time
import sys

# Custom imports 
from reports.MultiPage import MultiPage
from reports.location.location_report import location_report

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.set_page_config(
    page_title="2024 Asia Citadel Datathon",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Add all your applications (pages) here

app.add_page("Location", location_report)

app.run()