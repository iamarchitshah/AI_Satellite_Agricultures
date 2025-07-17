# 🌾 AI-Powered Satellite Image Analyzer for Agriculture

This project leverages satellite imagery and artificial intelligence to empower modern precision agriculture. It helps detect crop stress, predict yield, and recommend interventions using deep learning models and remote sensing data — all visualized through an interactive Streamlit dashboard.

---

## 🧠 Project Objective

- Detect crop health using NDVI and CNN segmentation
- Predict crop yield using time-series NDVI and LSTM
- Enable real-time insights using Google Earth Engine
- Provide farmer-focused suggestions (water, fertilizer)

---

## 🧩 Key Features

### 🛰️ 1. Crop Health Analyzer
- Upload NDVI `.tif` satellite images (e.g., Sentinel-2)
- Processes image using a trained **U-Net** segmentation model
- Highlights healthy vs. unhealthy crop regions
- Visual overlay of segmented crop stress areas

### 📈 2. Yield Predictor (CSV Upload)
- Upload NDVI time series data (`.csv` with NDVI values)
- Forecast crop yield in tons/hectare
- Uses LSTM (Long Short-Term Memory) model for prediction
- Chart to visualize NDVI over time

### 🌍 3. Yield Predictor (Map Auto-Fetch)
- Click any location on the world map
- NDVI time series is auto-fetched using **Google Earth Engine**
- Select start and end date range
- Instantly visualize NDVI trends and get yield prediction

---

## 🖥️ UI Dashboard

- Built using **Streamlit**
- Responsive tabs for different modules
- Real-time NDVI visualization
- Prediction overlays + exportable insights

---

## 🧰 Tech Stack

| Layer            | Tools/Tech                                   |
|------------------|----------------------------------------------|
| 🌐 Satellite Data | Google Earth Engine, Sentinel-2, Landsat     |
| 🧠 Models         | TensorFlow/Keras (U-Net, LSTM)               |
| 🖼️ Image Processing | OpenCV, Rasterio, GDAL, NumPy                 |
| 🌱 Visualization  | Streamlit, Folium, Matplotlib, Leaflet.js   |
| ☁️ Storage        | Firebase / AWS S3 / Local                    |
| 🧪 Language        | Python                                       |

---

## 📁 Project Structure

```
AI_Satellite_Agriculture/
├── app/
│   └── dashboard.py              # Streamlit multi-tab interface
├── models/
│   ├── unet_crop_health.h5       # Crop segmentation model (U-Net)
│   └── lstm_yield_predictor.h5   # Yield prediction model (LSTM)
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

---

## 🚀 How to Run It Locally

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AI-Satellite-Agriculture.git
cd AI-Satellite-Agriculture
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Authenticate Earth Engine
```bash
earthengine authenticate
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app/dashboard.py
```

---

## 📦 Requirements (from `requirements.txt`)

```
streamlit
streamlit-folium
folium
earthengine-api
tensorflow
scikit-learn
pandas
numpy
matplotlib
patchify
rasterio
```

---

## 📌 Use Cases

- Agriculture monitoring at scale
- Real-time field health alerts
- Government planning of crop yield
- Farmer advisory systems
- Academic and research applications

---

## 🔮 Future Enhancements

- 📲 Android mobile version with offline maps
- 🌐 Local language support (e.g., Hindi, Gujarati)
- 📡 Soil pH / IoT sensor integration
- 🛰️ Historical comparison of yield per region
- 📊 District-wise dashboards for policymakers

---

## 👥 Authors

- **Shah Archit**
- **Thakar Maitrey**

Department of Information Technology  
3rd Year, Semester 5 – Batch IT-2-D2  
Charotar University of Science and Technology  
Chandubhai S. Patel Institute of Technology

---

## 📜 License

This project is open-source for academic and non-commercial use only.  
For commercial licensing, contact the authors.

---

## ⭐ GitHub

If you found this helpful, leave a ⭐ on the repository!  
Let’s build tech for smarter, sustainable agriculture. 🌱
