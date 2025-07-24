import streamlit as st
import ee
import json
import geemap.foliumap as geemap

st.set_page_config(layout="wide", page_title="GEE Dashboard")

# Load service account info from Streamlit secrets
service_account_info = json.loads(st.secrets["GEE_SERVICE_JSON"])

# Authenticate Earth Engine
credentials = ee.ServiceAccountCredentials(
    email=service_account_info["client_email"],
    key_data=service_account_info
)
ee.Initialize(credentials)

st.title("🌍 Earth Engine Satellite Dashboard")

# Select region and dates
with st.sidebar:
    st.header("Controls")
    lat = st.number_input("Latitude", value=21.15)
    lon = st.number_input("Longitude", value=72.78)
    start_date = st.date_input("Start Date", value=ee.Date('2023-01-01').format('YYYY-MM-dd').getInfo())
    end_date = st.date_input("End Date", value=ee.Date('2023-12-31').format('YYYY-MM-dd').getInfo())

    show_ndvi = st.checkbox("Show NDVI", value=True)

# Create Earth Engine geometry
point = ee.Geometry.Point([lon, lat])
region = point.buffer(10000).bounds()  # 10km buffer

# Load Sentinel-2 imagery
s2 = ee.ImageCollection('COPERNICUS/S2_SR') \
    .filterDate(str(start_date), str(end_date)) \
    .filterBounds(region) \
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
    .median()

# Calculate NDVI
ndvi = s2.normalizedDifference(['B8', 'B4']).rename('NDVI')

# Create map
Map = geemap.Map(center=[lat, lon], zoom=10)

if show_ndvi:
    ndvi_params = {'min': 0.0, 'max': 1.0, 'palette': ['white', 'green']}
    Map.addLayer(ndvi, ndvi_params, 'NDVI')
    st.success("NDVI layer added to the map.")
else:
    vis_params = {'bands': ['B4', 'B3', 'B2'], 'min': 0, 'max': 3000}
    Map.addLayer(s2, vis_params, 'Sentinel-2 RGB')
    st.success("RGB image layer added to the map.")

# Display map
Map.to_streamlit(width=1200, height=600)

st.markdown("✅ Data source: Sentinel-2 Surface Reflectance")

