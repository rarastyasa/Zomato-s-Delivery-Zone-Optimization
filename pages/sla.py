# pages/sla.py
import streamlit as st
import pandas as pd
import os
import numpy as np

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans

# =======================
# CACHED LOADING
# =======================

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

@st.cache_resource
def build_preprocessor():
    num_features = ['Delivery_location_latitude', 'Delivery_location_longitude']
    cat_features = ['Road_traffic_density', 'Weather_conditions']

    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), num_features),
            ("cat", OneHotEncoder(drop="first"), cat_features)
        ]
    )

@st.cache_resource
def build_kmeans(df, _preprocessor):
    X = _preprocessor.fit_transform(df)
    model = KMeans(n_clusters=3, random_state=42)
    model.fit(X)
    return model


# =======================
# LOAD DATA
# =======================

current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "clustering_zomato.csv")
summary_path = os.path.join(current_dir, "..", "data", "cluster_summary.csv")

df_clean = load_csv(data_path)
df_summary = load_csv(summary_path)

preprocessor = build_preprocessor()
kmeans = build_kmeans(df_clean, preprocessor)


# =======================
# SLA PAGE
# =======================
def sla_page():
    st.title("⏱ Cluster & SLA Prediction Tool")

    st.markdown("""
    **SLA (Service Level Agreement)** estimates delivery time based on
    **location, traffic, and weather conditions**.
    """)

    # --------------------
    # USER INPUT
    # --------------------
    st.subheader("Input Delivery Conditions")

    lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=22.0)
    lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=68.0)
    traffic = st.selectbox("Traffic Condition", options=df_clean['Road_traffic_density'].unique())
    weather = st.selectbox("Weather Condition", options=df_clean['Weather_conditions'].unique())

    # --------------------
    # PREDICT CLUSTER
    # --------------------
    input_df = pd.DataFrame({
        'Delivery_location_latitude': [lat],
        'Delivery_location_longitude': [lon],
        'Road_traffic_density': [traffic],
        'Weather_conditions': [weather]
    })

    transformed_input = preprocessor.transform(input_df)
    cluster_pred = kmeans.predict(transformed_input)[0]

    # --------------------
    # SLA SUMMARY
    # --------------------
    if 'kmeans_cluster_features' in df_summary.columns:
        row = df_summary[df_summary['kmeans_cluster_features'] == cluster_pred]

        cluster_avg = row['avg_time'].values[0]
        cluster_std = row['std_dev'].values[0]
        sla_pred = cluster_avg + cluster_std

        readable_table = row.rename(columns={
            'kmeans_cluster_features': 'Cluster ID',
            'lat_mean': 'Avg Latitude',
            'lon_mean': 'Avg Longitude',
            'dominant_traffic': 'Dominant Traffic',
            'dominant_weather': 'Dominant Weather',
            'order_count_env': 'Number of Orders',
            'avg_time': 'Average Time (min)',
            'median_time': 'Median Time (min)',
            'std_dev': 'Std Dev (min)',
            'sla_time': 'SLA Time (min)'
        })[[
            'Cluster ID', 'Avg Latitude', 'Avg Longitude', 'Dominant Traffic',
            'Dominant Weather', 'Number of Orders', 'Average Time (min)',
            'Median Time (min)', 'Std Dev (min)', 'SLA Time (min)'
        ]]
    else:
        sla_pred, cluster_avg, cluster_std = np.nan, np.nan, np.nan
        readable_table = pd.DataFrame()

    # --------------------
    # OUTPUT EXPANDER
    # --------------------
    with st.expander("View Predicted SLA"):
        st.subheader("Predicted SLA")
        st.markdown(f"""
        **Predicted SLA Time:** `{sla_pred:.2f} min`  
        **Cluster ID:** `{cluster_pred}`  
        **Cluster Avg Time:** `{cluster_avg:.2f} min`  
        **Cluster Std Dev:** `{cluster_std:.2f} min`  
        """)

        st.markdown("""
        **Interpretation:**  
        The SLA uses the cluster’s average + one standard deviation to provide a safe and realistic
        delivery time estimate under varying weather & traffic conditions.
        """)

        st.markdown("### Cluster Details")
        st.table(readable_table)

    with st.expander("How to Use"):
        st.markdown("""
        1. Enter delivery coordinates.  
        2. Select traffic & weather conditions.  
        3. View the predicted SLA in the expander.  
        """)