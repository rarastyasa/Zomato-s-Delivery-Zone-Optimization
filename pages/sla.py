# pages/sla.py
import streamlit as st
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans

# Load Dataset
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "clustering_zomato.csv")
summary_path = os.path.join(current_dir, "..", "data", "cluster_summary.csv")

df_clean = pd.read_csv(data_path)
df_summary = pd.read_csv(summary_path)

# Preprocessing
num_features = ['Delivery_location_latitude', 'Delivery_location_longitude']
cat_features = ['Road_traffic_density', 'Weather_conditions']

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_features),
        ("cat", OneHotEncoder(drop="first"), cat_features)
    ]
)

df_cluster = preprocessor.fit_transform(df_clean)

# Fit KMeans
k_optimal = 3
kmeans = KMeans(n_clusters=k_optimal, random_state=42)
df_clean['kmeans_cluster_features'] = kmeans.fit_predict(df_cluster)

# SLA Prediction Tool
def sla_page():
    st.title("⏱ Cluster & SLA Prediction Tool")
    
    st.markdown("""
    **SLA (Service Level Agreement) Time**: Estimated time for a delivery to reach the customer based on location, traffic, and weather conditions.

    Use this tool to determine the predicted SLA and cluster based on your delivery input.
    """)

    #User Input
    st.subheader("Input Delivery Conditions")
    lat = st.number_input("Latitude", min_value=-90.0, max_value=90.0, value=22.0)
    lon = st.number_input("Longitude", min_value=-180.0, max_value=180.0, value=68.0)
    traffic = st.selectbox("Traffic Condition", options=df_clean['Road_traffic_density'].unique())
    weather = st.selectbox("Weather Condition", options=df_clean['Weather_conditions'].unique())

    # Predict Cluster 
    input_df = pd.DataFrame({
        'Delivery_location_latitude': [lat],
        'Delivery_location_longitude': [lon],
        'Road_traffic_density': [traffic],
        'Weather_conditions': [weather]
    })

    input_cluster = preprocessor.transform(input_df)
    cluster_pred = kmeans.predict(input_cluster)[0]

    # Get SLA from summary 
    if 'kmeans_cluster_features' in df_summary.columns:
        sla_row = df_summary[df_summary['kmeans_cluster_features'] == cluster_pred]
        cluster_avg = sla_row['avg_time'].values[0]
        cluster_std = sla_row['std_dev'].values[0]
        sla_pred = cluster_avg + cluster_std

        # Make readable table 
        readable_table = sla_row.rename(columns={
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
        })
        readable_table = readable_table[[
            'Cluster ID', 'Avg Latitude', 'Avg Longitude', 'Dominant Traffic', 'Dominant Weather',
            'Number of Orders', 'Average Time (min)', 'Median Time (min)', 'Std Dev (min)', 'SLA Time (min)'
        ]]
    else:
        cluster_avg, cluster_std, sla_pred = np.nan, np.nan, np.nan
        readable_table = pd.DataFrame()

    # Expander: Show Predicted SLA 
    with st.expander("View Predicted SLA"):
        st.subheader("Predicted SLA")
        st.markdown(f"""
        **Predicted SLA Time (minutes):** {sla_pred:.2f}  
        **Cluster ID:** {cluster_pred}  
        **Cluster Avg Time:** {cluster_avg:.2f} min  
        **Cluster Std Dev:** {cluster_std:.2f} min
        """)
        st.markdown(f"""
        **Interpretation:**  
        Your input falls into cluster **{cluster_pred}**, which groups deliveries by location, traffic, and weather. 
        The predicted SLA accounts for variability (**+1 std deviation**), giving an estimated delivery time of **{sla_pred:.2f} min**.
        """)

        st.markdown("### Cluster Details")
        st.table(readable_table)

    # Additional Info 
    with st.expander("How to use this tool"):
        st.markdown("""
        1. Enter the delivery location (latitude and longitude).  
        2. Select the traffic condition.  
        3. Select the weather condition.  
        4. Open the "View Predicted SLA" expander to see results.  

        This helps estimate delivery times and understand which cluster your delivery falls into.
        """)