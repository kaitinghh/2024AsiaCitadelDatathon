import streamlit as st
import os
import time
import sys

# Custom imports 
from reports.MultiPage import MultiPage
from reports.location.location_report import location_report
from reports.neighbor_migration.neighbor_migration_report import neighbor_migration_report
from reports.abroad_migration.abroad_migration_report import abroad_migration_report

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
app.add_page("Neighbor States Migration", neighbor_migration_report)
app.add_page("Abroad States Migration", abroad_migration_report)

app.run()