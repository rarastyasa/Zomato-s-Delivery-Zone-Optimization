# pages/map.py
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import os

# Load Dataset
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "clustering_zomato.csv")
df_clean = pd.read_csv(data_path)

# Load cluster summary CSV
summary_path = os.path.join(current_dir, "..", "data", "cluster_summary.csv")
df_summary = pd.read_csv(summary_path)

# Page Function
def map_page():
    st.title("🗺️ Delivery Zone Map with Clusters")

    # map centre point (mean customer location)
    center_lat = df_clean['Delivery_location_latitude'].mean()
    center_lon = df_clean['Delivery_location_longitude'].mean()

    # Base map-
    m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

    # MarkerCluster for eficiency
    marker_cluster = MarkerCluster().add_to(m)

    # Colors for each cluster
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 
              'lightred', 'beige', 'darkblue', 'darkgreen']

    # Plot points based on cluster
    for _, row in df_clean.iterrows():
        folium.CircleMarker(
            location=[row['Delivery_location_latitude'], row['Delivery_location_longitude']],
            radius=4,
            color=colors[row['kmeans_cluster_features'] % len(colors)],
            fill=True,
            fill_opacity=0.7,
            popup=f"Cluster: {row['kmeans_cluster_features']}"
        ).add_to(marker_cluster)

    # Fullscreen map
    st_folium(m, width="1000", height=550)

    # Cluster summary
    st.markdown("## 📊 Cluster Summary")
    st.dataframe(df_summary)
