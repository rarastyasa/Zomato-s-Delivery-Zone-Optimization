# 📍 Zomato Delivery Zone Optimization Using Geospatial Analytics

This project applies **geospatial analytics**, **clustering**, and **delivery performance analysis** to optimize Zomato’s delivery zones.  
By examining delivery locations, traffic density, weather patterns, and delivery times, this project identifies operational bottlenecks and proposes **cluster-based recommendations** to improve SLA, routing efficiency, and courier allocation.

🔗 **Live Streamlit App:**  
👉 https://zomato-s-delivery-zone-optimization.streamlit.app/

---

## 🚀 Project Overview

The main goal of this project is to **optimize delivery zones** by understanding spatial patterns and operational challenges across different regions.

Through geospatial clustering (K-Means), distance computation, and delivery time analysis, this project provides:

- Identification of **high-density delivery clusters**
- Measurement of **delivery distances** using the Haversine formula
- Analysis of **weather and traffic impacts** on delivery time
- **Cluster-specific operational insights** and SLA adjustments
- An interactive **Streamlit dashboard** that visualizes the entire analysis

This helps improve:
✔ SLA reliability  
✔ Routing efficiency  
✔ Courier productivity  
✔ Resource allocation and operational cost  

---

## 🗂️ Project Structure
```
📦 Zomato-s-Delivery-Zone-Optimization
│
├── data/
│   ├── clustering_zomato.csv
│   ├── cluster_summary.csv
│   └── Zomato Dataset.csv
│
├── pages/
│   ├── contact.py
│   ├── dashboard.py
│   ├── home.py
│   ├── map.py
│   └── sla.py
│
├── zomato_delivery.py         # Main Streamlit launcher
├── requirements.txt
└── README.md
```
---

## 🧠 Key Features

### 🔵 1. Geospatial Cluster Analysis
- K-Means clustering for delivery zones  
- Heatmaps & scatterplots showing customer density  
- Identification of delivery hotspots  

### 🟣 2. Distance & Time Optimization
- Haversine distance calculation  
- Distribution of delivery distance  
- Distance vs delivery time relationship  
- Detection of inefficiencies and anomalies  

### 🟠 3. Traffic & Weather Impact
- Weather condition distribution  
- Traffic density influence on delivery time  
- Boxplots, histograms, and pie charts  

### 🟢 4. Operational Recommendations (Cluster-Based)

| Cluster | Key Characteristics | Challenges | Recommendations |
|--------|----------------------|------------|----------------|
| **0 – West-Central (Fog)** | High-density (19k+), foggy, low traffic | Visibility risks | Hotspot rider placement, route optimization, stable SLA |
| **1 – South-Central (Stormy)** | Large region (16k+), storm-prone | Weather delays | SLA buffer, real-time storm alerts, safety-first routing |
| **2 – East Region (Sandstorms)** | Smallest region (4k), long distances | Sandstorm disruptions | Extra fleet, flexible scheduling, extended SLA |

---

## 🗺️ Interactive Streamlit Dashboard

The dashboard includes:

### ✔ Geospatial Map  
- Cluster visualization  
- Region boundaries  
- Delivery density maps  

### ✔ Performance Dashboard  
- Delivery distance distribution  
- Delivery time histogram  
- Weather & traffic condition impacts  
- City-wise delivery performance  

### ✔ SLA-Based Insights  
- SLA time segmentation  
- Operational bottlenecks  
- Cluster summaries  

👉 **Try it live:**  
https://zomato-s-delivery-zone-optimization.streamlit.app/

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Pandas, NumPy**
- **Matplotlib, Seaborn**
- **Folium (via streamlit-folium)**
- **scikit-learn (KMeans)**
- **Geospatial analytics (Haversine Distance)**

---

## ▶️ How to Run Locally

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your_username>/Zomato-Delivery-Zone-Optimization.git
cd Zomato-Delivery-Zone-Optimization
```
### 2️⃣ Install Dependencies
``` bash
pip install -r requirements.txt
```
3️⃣ Run the Streamlit App
``` bash
streamlit run zomato_delivery.py
```

---
## 📓 Notebook Reference

The full exploratory workflow — including geospatial analysis, clustering, feature engineering, and delivery performance evaluation — is documented in the following notebook:

**`Take_Home_Test_Data_Science_Notebook.ipynb`**

This notebook serves as the analytical backbone of the project, containing all intermediate steps before deployment into the Streamlit dashboard.


---

## 💡 Business Impact Summary

This project delivers **data-driven insights** that directly improve operational performance across multiple dimensions:

### 🚀 Key Operational Improvements
- ⚡ **Faster delivery times** through optimized routing and better zone planning  
- 📊 **More consistent operations** using SLA calibration tailored per cluster  
- 🛵 **Higher fleet efficiency** by strategically positioning couriers based on demand patterns  
- 💸 **Reduced operational costs** through improved route allocation and resource planning  
- 😊 **Better customer experience** from more predictable and reliable delivery times  

These insights provide a strong foundation for strategic decision-making, ensuring delivery operations are both scalable and efficient.









