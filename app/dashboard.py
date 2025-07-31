import streamlit as st
import ee
import json
import folium
from streamlit_folium import st_folium

# 🌐 Authenticate using GEE service account
gee_service_json = st.secrets["GEE_SERVICE_JSON"]

# Convert the JSON string from secrets to dict
if isinstance(gee_service_json, str):
    service_account_info = json.loads(gee_service_json)
else:
    service_account_info = gee_service_json

# Convert back to JSON string for authentication
service_account_json_str = json.dumps(service_account_info)

# Authenticate and initialize Earth Engine
credentials = ee.ServiceAccountCredentials(
    service_account_info['client_email'], key_data=service_account_json_str
)
ee.Initialize(credentials)

# 📍 Define location and visualization parameters
lat, lon = 20.5937, 78.9629  # Center of India
image = ee.Image('COPERNICUS/S2_SR/20210623T104031_20210623T104028_T31TFJ').select('B4')
vis_params = {"min": 0, "max": 3000, "palette": ["blue", "green", "red"]}

# 🗺️ Add Earth Engine layer support to Folium
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

# 🎨 Create and display the map
m = folium.Map(location=[lat, lon], zoom_start=6)
m.add_ee_layer(image, vis_params, "Sentinel-2 Red Band")
folium.LayerControl().add_to(m)

st.title("🌾 Satellite Imagery Viewer with GEE")
st.write("Displaying Sentinel-2 Red Band Image")
st_data = st_folium(m, width=700, height=500)
