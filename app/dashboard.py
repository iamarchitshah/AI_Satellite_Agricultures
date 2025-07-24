import streamlit as st
import json
import ee
import geemap.foliumap as geemap

st.set_page_config(layout="wide")
st.title("🛰️ Satellite-Based Agriculture Monitoring Dashboard")

# Authenticate with Google Earth Engine
try:
    service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])
    credentials = ee.ServiceAccountCredentials(
        email=service_account_info['client_email'],
        key_data=service_account_info
    )
    ee.Initialize(credentials)
    st.success("✅ Earth Engine initialized successfully.")
except Exception as e:
    st.error("❌ Failed to initialize Earth Engine.")
    st.exception(e)
    st.stop()

# Create a map
try:
    Map = geemap.Map(center=[20.5937, 78.9629], zoom=5)
    Map.add_basemap("SATELLITE")

    # Example: Load NDVI layer for agriculture monitoring
    collection = ee.ImageCollection('MODIS/006/MOD13Q1').select('NDVI')
    image = collection.sort('system:time_start', False).first()
    vis_params = {'min': 0, 'max': 9000, 'palette': ['white', 'green']}
    Map.addLayer(image, vis_params, "Latest NDVI")

    # Display the map
    Map.to_streamlit(height=600)

except Exception as e:
    st.error("❌ Failed to load satellite imagery.")
    st.exception(e)
