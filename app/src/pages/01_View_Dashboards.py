import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks
import requests

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

# set the header of the page
st.header('Dashboards')

st.write('##### Here are the dashboards available to you.')

# Get Dashboards from api
def get_dashboards(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching dashboards: {e}")
        return []

api_url = "http://web-api:4000/d/dashboard"
dashboards = get_dashboards(api_url)
if dashboards:
    df = pd.DataFrame(dashboards)
    st.dataframe(df, hide_index=True)
else:
    st.write("No dashboards available.")
