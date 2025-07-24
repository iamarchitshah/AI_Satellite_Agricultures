import streamlit as st
import json
import ee
import folium
from streamlit_folium import st_folium
from folium import Map, Marker

# -------------------- Setup Page --------------------
st.set_page_config(page_title="Satellite Agriculture NDVI", layout="wide")
st.title("🌾 Satellite-Based Agriculture Analysis")
st.markdown("Click on the map to select a location and view NDVI values from satellite data.")

# -------------------- Authenticate with Earth Engine --------------------
service_json = st.secrets["GEE_SERVICE_JSON"]

# Convert secret string to dictionary
if isinstance(service_json, str):
    service_account_info = json.loads(service_json)
else:
    service_account_info = service_json

# Initialize Earth Engine
credentials = ee.ServiceAccountCredentials(
    service_account_info["client_email"],
    key_data=json.dumps(service_account_info)
)
ee.Initialize(credentials)

# -------------------- Folium Map Setup --------------------
def create_map():
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5)  # Default: India center
    folium.Marker([22.9734, 78.6569], tooltip="Click on map to select location").add_to(m)
    return m

st.markdown("### 🗺️ Select a location on the map:")
map_data = st_folium(create_map(), height=400, width=700)

# Get clicked coordinates
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success(f"Selected Location: {lat:.4f}, {lon:.4f}")

    # -------------------- NDVI Analysis --------------------
    point = ee.Geometry.Point([lon, lat])

    # Sentinel-2 NDVI
    collection = (ee.ImageCollection("COPERNICUS/S2_SR")
                  .filterBounds(point)
                  .filterDate("2023-01-01", "2023-12-31")
                  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10)))

    def add_ndvi(image):
        ndvi = image.normalizedDifference(["B8", "B4"]).rename("NDVI")
        return image.addBands(ndvi)

    with_ndvi = collection.map(add_ndvi)
    ndvi_stats = with_ndvi.select("NDVI").mean().reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point,
        scale=10
    )

    ndvi_value = ndvi_stats.get("NDVI").getInfo() if ndvi_stats.get("NDVI") else None

    if ndvi_value is not None:
        st.metric(label="🌿 Average NDVI at this Location", value=f"{ndvi_value:.3f}")
    else:
        st.warning("No NDVI data found for this point.")
else:
    st.info("Click anywhere on the map above to get NDVI data.")
