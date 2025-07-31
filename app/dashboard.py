import streamlit as st
import ee
import json
import os
from streamlit_folium import st_folium
import folium

# Load the GEE service account key from secrets
gee_service_json = st.secrets["GEE_SERVICE_JSON"]

# Convert JSON string to dict
if isinstance(gee_service_json, str):
    service_account_info = json.loads(gee_service_json)
else:
    service_account_info = gee_service_json  # If it's already a dict

# Authenticate with Earth Engine
credentials = ee.ServiceAccountCredentials(service_account_info['client_email'], key_data=service_account_info)
ee.Initialize(credentials)

# Streamlit App UI
st.title("🌍 Google Earth Engine Map Viewer")

st.write("This app uses a service account to authenticate with Google Earth Engine.")

# Example GEE dataset
image = ee.Image('COPERNICUS/S2_SR/20210623T104031_20210623T104028_T31TFJ').select('B4')

# Define map center
lat, lon = 48.858844, 2.294351  # Eiffel Tower

# Create a folium map
m = folium.Map(location=[lat, lon], zoom_start=12)

# Add Earth Engine layer
def add_ee_layer(self, ee_image_object, vis_params, name):
    map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
    folium.raster_layers.TileLayer(
        tiles=map_id_dict['tile_fetcher'].url_format,
        attr='Google Earth Engine',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

folium.Map.add_ee_layer = add_ee_layer

# Visualization parameters
vis_params = {
    'min': 0,
    'max': 3000,
    'palette': ['blue', 'green', 'red']
}

m.add_ee_layer(image, vis_params, "Sentinel-2 Red Band")
folium.LayerControl().add_to(m)

# Display map in Streamlit
st_folium(m, width=700, height=500)
