import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
from patchify import patchify
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import folium
from streamlit_folium import st_folium
import json
import ee
from datetime import datetime

# ✅ Initialize Earth Engine using service account from secrets
service_account_info = json.loads(st.secrets["GEE_SERVICE_JSON"])
credentials = ee.ServiceAccountCredentials(
    service_account_info["client_email"],
    key_data=service_account_info
)
ee.Initialize(credentials)



# 🔄 Load models once
@st.cache_resource
def load_unet():
    return load_model("models/unet_crop_health.h5")

@st.cache_resource
def load_lstm():
    return load_model("models/lstm_yield_predictor.h5")

# 🔍 Fetch NDVI Time Series from Google Earth Engine
def fetch_ndvi_series(lat, lon, start_date, end_date):
    point = ee.Geometry.Point([lon, lat])
    collection = (ee.ImageCollection("COPERNICUS/S2")
                  .filterDate(start_date, end_date)
                  .filterBounds(point)
                  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
                  .map(lambda img: img.normalizedDifference(['B8', 'B4']).rename('NDVI')))

    def reduce(img):
        return img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=point,
            scale=10
        ).set('system:time_start', img.get('system:time_start'))

    series = collection.map(reduce).getInfo()
    ndvi_values, dates = [], []
    for feat in series['features']:
        props = feat['properties']
        ndvi = props.get('NDVI')
        ts = props.get('system:time_start')
        if ndvi is not None:
            ndvi_values.append(ndvi)
            dates.append(datetime.utcfromtimestamp(ts / 1000))
    return pd.DataFrame({'Date': dates, 'NDVI': ndvi_values})

# 🧭 App UI Layout
st.set_page_config(layout="wide", page_title="Satellite Crop Analyzer")

st.title("🌾 AI-Powered Satellite Image Analyzer")

tab1, tab2, tab3 = st.tabs(["🛰️ Crop Health Analyzer", "📈 Yield from CSV", "🌍 Yield from Map"])

# ------------------ TAB 1: Upload NDVI TIF & Segment ----------------------
with tab1:
    st.subheader("🛰 Upload NDVI .tif Image for Crop Health Segmentation")
    file = st.file_uploader("Upload NDVI GeoTIFF", type=["tif", "tiff"])

    if file:
        with rasterio.open(file) as src:
            ndvi = src.read(1)
        st.image(ndvi, caption="Uploaded NDVI Image", use_column_width=True)
        ndvi = np.clip(ndvi, 0, 1)

        model = load_unet()
        patch_size = 128
        if ndvi.shape[0] % patch_size == 0 and ndvi.shape[1] % patch_size == 0:
            patches = patchify(ndvi, (patch_size, patch_size), step=patch_size)
            prediction = np.zeros_like(ndvi)

            for i in range(patches.shape[0]):
                for j in range(patches.shape[1]):
                    patch = patches[i, j, :, :]
                    input_patch = np.expand_dims(np.expand_dims(patch, 0), -1)
                    pred = model.predict(input_patch)[0, :, :, 0]
                    prediction[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size] = (pred > 0.5)

            st.image(prediction, caption="🟢 Predicted Crop Health Mask", use_column_width=True)
        else:
            st.warning("Image dimensions must be divisible by 128 (e.g., 512x512, 1024x1024)")

# ------------------ TAB 2: Upload CSV for Yield Prediction ----------------------
with tab2:
    st.subheader("📈 Upload NDVI Time Series CSV for Yield Prediction")
    csv = st.file_uploader("Upload NDVI CSV", type="csv")

    if csv:
        df = pd.read_csv(csv)
        series = df.values.reshape(-1, 1)
        st.line_chart(series, use_container_width=True)

        scaler = MinMaxScaler()
        norm_series = scaler.fit_transform(series)
        X = np.expand_dims(norm_series, axis=0)

        model = load_lstm()
        pred_yield = model.predict(X)[0][0]
        st.success(f"🌾 Predicted Yield: **{pred_yield:.2f} tons/hectare**")

# ------------------ TAB 3: Click Map to Predict Yield ----------------------
with tab3:
    st.subheader("🌍 Click Map to Auto-Fetch NDVI and Predict Yield")
    st.markdown("🗺️ Click your farm location on the map")

    default_location = [22.3072, 73.1812]
    m = folium.Map(location=default_location, zoom_start=6)
    m.add_child(folium.LatLngPopup())
    map_data = st_folium(m, height=500, width=800)

    if map_data and map_data.get("last_clicked"):
        coords = map_data["last_clicked"]
        lat, lon = coords["lat"], coords["lng"]
        st.success(f"📍 Selected location: ({lat:.4f}, {lon:.4f})")

        col1, col2 = st.columns(2)
        with col1:
            start = st.date_input("Start Date", datetime(2023, 6, 1))
        with col2:
            end = st.date_input("End Date", datetime(2023, 10, 1))

        if st.button("Fetch NDVI & Predict Yield"):
            df = fetch_ndvi_series(lat, lon, str(start), str(end))

            if df.empty or len(df) < 10:
                st.warning("Not enough NDVI data found. Try adjusting the date range.")
            else:
                st.line_chart(df.set_index("Date")["NDVI"])
                series = df["NDVI"].values.reshape(-1, 1)

                scaler = MinMaxScaler()
                series_norm = scaler.fit_transform(series)
                X = np.expand_dims(series_norm, axis=0)

                model = load_lstm()
                pred_yield = model.predict(X)[0][0]
                st.success(f"🌾 Predicted Yield: **{pred_yield:.2f} tons/hectare**")
