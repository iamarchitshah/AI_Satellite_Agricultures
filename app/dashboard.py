import streamlit as st
import ee
import json

# Title of the app
st.title("🌍 Google Earth Engine with Streamlit")

# Authenticate and initialize Earth Engine
try:
    # Load GEE service account credentials from Streamlit secrets
    service_account_info = json.loads(st.secrets["GEE_SERVICE_JSON"])

    # Authenticate using service account credentials
    credentials = ee.ServiceAccountCredentials(
        email=service_account_info["client_email"],
        key_data=service_account_info
    )
    ee.Initialize(credentials)
    st.success("✅ Successfully authenticated with Google Earth Engine!")

except Exception as e:
    st.error(f"❌ Google Earth Engine authentication failed:\n{e}")
    st.stop()

# Example: Display info about an Earth Engine dataset
try:
    # Load a sample EE dataset (MODIS land surface temperature)
    dataset = ee.ImageCollection("MODIS/006/MOD11A2").select('LST_Day_1km')

    # Get time range info
    first_image = dataset.first()
    info = first_image.getInfo()

    # Show metadata
    st.subheader("📦 Example Dataset: MODIS Land Surface Temp")
    st.write(info)

except Exception as e:
    st.error(f"⚠️ Failed to load EE dataset:\n{e}")
