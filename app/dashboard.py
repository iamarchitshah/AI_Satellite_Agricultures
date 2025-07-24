import streamlit as st
import ee
import json
import geemap

st.set_page_config(page_title="AI Satellite Agriculture", layout="wide")

# Title
st.title("🌾 AI Satellite Agriculture Dashboard")

# Load service account JSON from Streamlit secrets
service_account_info = st.secrets["GEE_SERVICE_JSON"]
key_data_json = json.dumps(service_account_info)

# Authenticate with Google Earth Engine
credentials = ee.ServiceAccountCredentials(
    email=service_account_info["client_email"],
    key_data=key_data_json
)
ee.Initialize(credentials)

# Sidebar inputs
st.sidebar.header("🔧 Controls")
region = st.text_input("Enter a region name (e.g., 'India')", "India")
start_date = st.date_input("Start Date", value=None)
end_date = st.date_input("End Date", value=None)

# Sentinel-2 NDVI
try:
    geometry = ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017") \
        .filter(ee.Filter.eq('country_na', region)) \
        .geometry()

    collection = (ee.ImageCollection("COPERNICUS/S2_SR")
                  .filterDate(str(start_date), str(end_date))
                  .filterBounds(geometry)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                  .median())

    ndvi = collection.normalizedDifference(['B8', 'B4']).rename('NDVI')

    m = geemap.Map(center=[20, 78], zoom=4)  # You can adjust the center
    ndvi_vis = {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}
    m.addLayer(ndvi, ndvi_vis, 'NDVI')
    m.addLayer(geometry, {}, 'Region Boundary')
    m.addLayerControl()

    m.to_streamlit(height=600)

except Exception as e:
    st.error("Failed to load data:")
    st.code(str(e))
