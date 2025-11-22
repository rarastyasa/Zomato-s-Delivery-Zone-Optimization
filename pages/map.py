# pages/map.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import os

# CACHED LOADING
@st.cache_data
def load_clean_data(path):
    return pd.read_csv(path)

@st.cache_data
def load_summary(path):
    return pd.read_csv(path)

# LOAD DATA
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "clustering_zomato.csv")
summary_path = os.path.join(current_dir, "..", "data", "cluster_summary.csv")

df_clean = load_clean_data(data_path)
df_summary = load_summary(summary_path)

# PAGE FUNCTION
def map_page():
    st.title("🗺️ Delivery Zone Map with Clusters")

    # Center map
    center_lat = df_clean['Delivery_location_latitude'].mean()
    center_lon = df_clean['Delivery_location_longitude'].mean()

    # Base map
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    # Marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Colors for clusters
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
              'lightred', 'beige', 'darkblue', 'darkgreen']

    # Plot points
    for _, row in df_clean.iterrows():
        folium.CircleMarker(
            location=[row['Delivery_location_latitude'], row['Delivery_location_longitude']],
            radius=4,
            color=colors[row['kmeans_cluster_features'] % len(colors)],
            fill=True,
            fill_opacity=0.7,
            popup=f"Cluster: {row['kmeans_cluster_features']}"
        ).add_to(marker_cluster)

    # Display map
    st_folium(m, width=1000, height=550)

    # Cluster summary
    st.markdown("## 📊 Cluster Summary")
    st.dataframe(df_summary)
