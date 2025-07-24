import streamlit as st
import ee
import geemap.foliumap as geemap

# Page config
st.set_page_config(page_title="Satellite Agriculture Dashboard", layout="wide")
st.title("🌾 Satellite Agriculture Monitoring Dashboard")

# 🔐 Embedded GEE Service Account Credentials (replace placeholders!)
service_account_info = {
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "your-private-key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\nYOUR_PRIVATE_KEY\\n-----END PRIVATE KEY-----\\n",
  "client_email": "your-service-account@your-project-id.iam.gserviceaccount.com",
  "client_id": "your-client-id",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project-id.iam.gserviceaccount.com"
}

# ✅ Authenticate with Earth Engine
credentials = ee.ServiceAccountCredentials(
    email=service_account_info["client_email"],
    key_data=service_account_info
)
ee.Initialize(credentials)

# 🗺️ Create Earth Engine map centered on India
Map = geemap.Map(center=[20.5937, 78.9629], zoom=5)

# 🛰️ Load Sentinel-2 image and calculate NDVI
dataset = ee.ImageCollection("COPERNICUS/S2") \
    .filterDate("2023-01-01", "2023-12-31") \
    .filterBounds(ee.Geometry.Point(78.9629, 20.5937)) \
    .sort("CLOUDY_PIXEL_PERCENTAGE") \
    .first()

ndvi = dataset.normalizedDifference(['B8', 'B4']).rename('NDVI')

# 🖼️ NDVI visualization style
ndvi_vis = {
    'min': 0,
    'max': 1,
    'palette': ['white', 'green']
}

# 🧭 Add NDVI layer to map
Map.addLayer(ndvi, ndvi_vis, 'NDVI (2023)')
Map.addLayerControl()

# 📍 Streamlit map display
st.subheader("Normalized Difference Vegetation Index (NDVI) - Sentinel-2")
Map.to_streamlit(height=600)
