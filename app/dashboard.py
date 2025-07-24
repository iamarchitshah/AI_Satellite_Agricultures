import geemap

import streamlit as st
import ee
import json

st.set_page_config(page_title="AI Satellite Agriculture", layout="wide")

# Title
st.title("🌾 AI Satellite Agriculture Dashboard")

# Load service account JSON from Streamlit secrets (already parsed as dict)
service_account_info = st.secrets["GEE_SERVICE_JSON"]

# Convert dict to JSON string (as required by ee.ServiceAccountCredentials)
key_data_json = json.dumps(service_account_info)

# Authenticate with Earth Engine
credentials = ee.ServiceAccountCredentials(
    email=service_account_info["client_email"],
    key_data=key_data_json
)
ee.Initialize(credentials)

# Sidebar instructions
st.sidebar.header("🔧 Controls")
st.sidebar.write("Select parameters and visualize satellite data.")

# Main app
st.subheader("🛰️ NDVI Visualization from Sentinel-2")

# Region selector
region = st.text_input("Enter a region name or coordinates (e.g. 'India', '10,76')", "India")

# Date range
start_date = st.date_input("Start Date", value=ee.Date("2023-01-01").format().getInfo())
end_date = st.date_input("End Date", value=ee.Date("2023-12-31").format().getInfo())

# Fetch Sentinel-2 imagery
try:
    collection = (ee.ImageCollection("COPERNICUS/S2_SR")
                  .filterDate(str(start_date), str(end_date))
                  .filterBounds(ee.Geometry.Point([76, 10]))
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
                  .median()
                  .clipToCollection(ee.FeatureCollection("USDOS/LSIB_SIMPLE/2017").filter(ee.Filter.eq('country_na', region))))

    # Calculate NDVI
    ndvi = collection.normalizedDifference(['B8', 'B4']).rename('NDVI')

    # Display map
    m = geemap.Map(center=[10, 76], zoom=5)
    ndvi_params = {'min': 0, 'max': 1, 'palette': ['blue', 'white', 'green']}
    m.addLayer(ndvi, ndvi_params, 'NDVI')
    m.addLayerControl()
    m.to_streamlit(height=600)

except Exception as e:
    st.error("⚠️ Error loading Earth Engine data:")
    st.code(str(e))
