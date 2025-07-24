import streamlit as st
import ee
import geemap.foliumap as geemap
import json

# Set page configuration
st.set_page_config(
    page_title="Satellite Agriculture Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌾 Satellite Agriculture Monitoring Dashboard")

# Load credentials from secrets
try:
    service_account_info = st.secrets["GEE_SERVICE_JSON"]
    service_account_json = json.dumps(dict(service_account_info))
    credentials = ee.ServiceAccountCredentials(email=service_account_info["client_email"], key_data=service_account_json)
    ee.Initialize(credentials)
except Exception as e:
    st.error(f"Google Earth Engine authentication failed: {e}")
    st.stop()

# Sidebar controls
st.sidebar.title("🧭 Map Settings")
selected_basemap = st.sidebar.selectbox("🌍 Select Basemap", ["SATELLITE", "HYBRID", "TERRAIN", "ROADMAP"])

st.sidebar.markdown("---")
st.sidebar.write("Example Dataset:")
dataset_type = st.sidebar.radio("Choose dataset", ["MODIS NDVI", "Sentinel-2 NDVI"])

# Create Map
m = geemap.Map(center=[22.9734, 78.6569], zoom=5)
m.add_basemap(selected_basemap)

# Load and visualize NDVI data
if dataset_type == "MODIS NDVI":
    collection = ee.ImageCollection("MODIS/006/MOD13A1").select('NDVI').filterDate('2023-01-01', '2023-12-31')
    image = collection.mean()
    vis_params = {
        'min': 0.0,
        'max': 9000.0,
        'palette': ['white', 'green']
    }
    m.addLayer(image, vis_params, "MODIS NDVI (2023)")

elif dataset_type == "Sentinel-2 NDVI":
    collection = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterDate('2023-01-01', '2023-12-31') \
        .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10)) \
        .median()

    ndvi = collection.normalizedDifference(['B8', 'B4'])
    vis_params = {
        'min': 0.0,
        'max': 1.0,
        'palette': ['brown', 'yellow', 'green']
    }
    m.addLayer(ndvi, vis_params, "Sentinel-2 NDVI (2023)")

# Show Map
m.to_streamlit(height=600)

# Footer
st.markdown("---")
st.markdown("📍 Data Source: Google Earth Engine | 🛰️ MODIS & Sentinel-2")
