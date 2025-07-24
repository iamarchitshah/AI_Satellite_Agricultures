import streamlit as st
import json
import ee
import geemap.foliumap as geemap

# Load service account credentials from Streamlit secrets
service_account_info = json.loads(st.secrets["gcp_service_account"]["json"])

# Authenticate with Google Earth Engine
credentials = ee.ServiceAccountCredentials(
    email=service_account_info['client_email'],
    key_data=service_account_info
)
ee.Initialize(credentials)

# Streamlit UI
st.set_page_config(page_title="Satellite Agriculture Dashboard", layout="wide")
st.title("🌾 Satellite Agriculture Monitoring Dashboard")

# Create Earth Engine Map
Map = geemap.Map(center=[20.5937, 78.9629], zoom=4)

# Example: Load NDVI image from Sentinel-2
dataset = ee.ImageCollection("COPERNICUS/S2") \
    .filterDate("2023-01-01", "2023-12-31") \
    .filterBounds(ee.Geometry.Point(78.9629, 20.5937)) \
    .sort("CLOUDY_PIXEL_PERCENTAGE") \
    .first()

ndvi = dataset.normalizedDifference(['B8', 'B4']).rename('NDVI')
ndvi_vis = {
    'min': 0,
    'max': 1,
    'palette': ['white', 'green']
}
Map.addLayer(ndvi, ndvi_vis, 'NDVI 2023')
Map.addLayerControl()

st.markdown("### Example NDVI Visualization for Sentinel-2 (2023)")
Map.to_streamlit(height=600)
