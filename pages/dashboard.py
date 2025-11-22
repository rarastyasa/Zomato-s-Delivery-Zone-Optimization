# pages/dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Load dataset
current_dir = os.path.dirname(__file__)
data_path = os.path.join(current_dir, "..", "data", "clustering_zomato.csv")
df_clean = pd.read_csv(data_path)

# Haversine Distance Function
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

# Calculate distance_km
df_clean["distance_km"] = haversine(
    df_clean["Restaurant_latitude"],
    df_clean["Restaurant_longitude"],
    df_clean["Delivery_location_latitude"],
    df_clean["Delivery_location_longitude"]
)

# Dashboard Page Function
def dashboard_page():
    st.title("📊 Zomato Delivery Dashboard")

    # Row 1: Geospatial Distribution Analysis
    st.markdown("## 1. Geospatial Distribution Analysis")
    col1, col2 = st.columns(2)

    base_color = "#5f6075"
    custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom_map", 
    ["#d6d7de", "#a3a4b3", base_color],   # light → medium → dark
    N=256)

    # Scatter Plot
    with col1:
        st.markdown("### Customer Delivery Locations")
        fig1, ax1 = plt.subplots(figsize=(6,5))
        ax1.scatter(
            df_clean['Delivery_location_longitude'],
            df_clean['Delivery_location_latitude'],
            s=5, alpha=0.4, color="#5f6075"
        )
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")
        ax1.set_title("Customer Delivery Locations")
        st.pyplot(fig1)

        with st.expander("Insight"):
            st.markdown("""
    The scatter plot shows the distribution of customer locations based on longitude and latitude coordinates. Several clusters appear around longitude 73–76 and latitude 18–22, while some points are more isolated, potentially affecting delivery efficiency.
            """)

    # Heatmap
    with col2:
        st.markdown("### Delivery Density Heatmap")
        fig2, ax2 = plt.subplots(figsize=(6,5))
        sns.kdeplot(
            x=df_clean['Delivery_location_longitude'],
            y=df_clean['Delivery_location_latitude'],
            cmap=custom_cmap, 
            fill=True, 
            bw_method=0.3, 
            alpha=0.8,
            ax=ax2
        )

        ax2.set_xlabel("Longitude")
        ax2.set_ylabel("Latitude")
        ax2.set_title("Delivery Density Heatmap")
        st.pyplot(fig2)

        with st.expander("Insight"):
            st.markdown("""
    The heatmap highlights delivery density, with the strongest concentration around longitude 72–76 and latitude 18–22. Several medium-density zones appear around 75–78 and 24–28.
            """)

    # Row 2: Distance Analysis ---
    st.markdown("## 2. Distance Analysis")
    col1, col2 = st.columns(2)

    # Distribution of Delivery Distance (Bar Chart)
    with col1:
        st.markdown("### Distribution of Delivery Distance")
        distance_counts = df_clean['distance_km'].round().value_counts().sort_index()
        fig3, ax3 = plt.subplots(figsize=(6,5))
        ax3.bar(distance_counts.index, distance_counts.values, color="#5f6075")  # light blue
        ax3.set_xlabel("Distance (km)")
        ax3.set_ylabel("Frequency")
        ax3.set_title("Delivery Distance Distribution")
        fig3.tight_layout()
        st.pyplot(fig3, use_container_width=False)

        with st.expander("Insight"):
            st.markdown("""
The histogram shows a fairly spread distribution of delivery distances, ranging from around 2 km to more than 20 km, with most deliveries falling within the 5–15 km range.
        """)


    # Distance vs Delivery Time Scatter
    with col2:
        st.markdown("### Distance vs Delivery Time")
        fig4, ax4 = plt.subplots(figsize=(6,5))
        ax4.scatter(df_clean["distance_km"], df_clean["Time_taken (min)"], alpha=0.6, color="#5f6075")
        ax4.set_xlabel("Distance (km)")
        ax4.set_ylabel("Delivery Time (min)")
        ax4.set_title("Distance vs Delivery Time")
        fig4.tight_layout()  
        st.pyplot(fig4, use_container_width=False)  

        with st.expander("Insight"):
            st.markdown("""
The scatter plot shows the relationship between delivery distance and delivery time, where it generally appears that the greater the distance, the greater the variation in delivery time, but there is no strong linear pattern. The data points are scattered quite widely in each distance category, indicating that delivery time is influenced not only by distance but also by other factors such as traffic conditions, routes, or courier efficiency. Although there is a slight tendency for delivery time to increase with greater distance, the spread remains high, so the relationship between the variables can be said to be weak and inconsistent.
            """)
    
    # Row 3: Delivery Time & Delay Analysis
    st.markdown("## 3. Delivery Time & Delay Analysis")

    # Row 1: Plot 1 & Plot 4
    col1, col2 = st.columns(2)

    # Plot 1: Distribution of Time Taken
    with col1:
        st.markdown("### Distribution of Time Taken")
        time_counts = df_clean["Time_taken (min)"].round().value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(6,5))
        ax1.bar(time_counts.index, time_counts.values, color="#5f6075")  # light blue
        ax1.set_xlabel("Time Taken (min)")
        ax1.set_ylabel("Frequency")
        ax1.set_title("Delivery Time Distribution")
        fig1.tight_layout()
        st.pyplot(fig1, use_container_width=False)
        with st.expander("Insight"):
            st.markdown("""
The bar chart shows the distribution of time taken for delivery. The range of time taken is between 10 and 60 minutes, with the majority of deliveries taking between 15 and 30 minutes.
            """)

    # Plot 4: Time taken by Weather Conditions
    with col2:
        st.markdown("### Delivery Time by Weather Conditions")
        fig4, ax4 = plt.subplots(figsize=(6,5))
        colors_soft_blue = ["#5f6075", "#3c3c50", "#9e8c75", "#e4e4e4", "#fcf7f6", "#667b8a"]
        unique_weather = df_clean["Weather_conditions"].unique()
        palette = {weather: color for weather, color in zip(unique_weather, colors_soft_blue)}
        sns.boxplot(
            data=df_clean, 
            x="Weather_conditions", 
            y="Time_taken (min)", 
            ax=ax4,
            palette=palette
        )
        ax4.set_title("Delivery Time by Weather")
        ax4.set_xlabel("Weather")
        ax4.set_ylabel("Time Taken (min)")
        ax4.tick_params(axis='x', rotation=45)
        fig4.tight_layout()

        st.pyplot(fig4, use_container_width=False)

        with st.expander("Insight"):
            st.markdown("""
    **Longest Delivery Time (Highest Median)**: Foggy and cloudy conditions show the longest median delivery time, around 30–35 minutes.  

    **Fastest Delivery Time (Lowest Median)**: Sunny conditions have the fastest median delivery time (~18 minutes).  

    **Variability & Outliers**: Stormy, Sandstorms, and Windy conditions have similar medians (25–30 mins), with outliers indicating extreme delays.
            """)

    # Row 2: Plot 2
    st.markdown("### Time Taken by City")
    cities = df_clean["City"].unique()
    fig2, axes2 = plt.subplots(1, len(cities), figsize=(6*len(cities),5))
    if len(cities) == 1:
        axes2 = [axes2]  

    for ax, city_name in zip(axes2, cities):
        city_data = df_clean[df_clean["City"] == city_name]
        sns.histplot(data=city_data, x="Time_taken (min)", kde=True, color="#5f6075", ax=ax)
        ax.set_title(f"{city_name}")
        ax.set_xlabel("Time Taken (min)")
        ax.set_ylabel("Frequency")

    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=False)
    with st.expander("Insight"):
        st.markdown("""
1. **Metropolitan**: Most deliveries 20–35 min, relatively stable despite high volume.  
2. **Urban**: Faster deliveries 10–20 min, but long tail up to 50 min.  
3. **Semi-Urban**: Slower 44–54 min but consistent, smaller dataset.
        """)

    # Row 3: Plot 3
    st.markdown("### Time Taken by Traffic Density")
    traffic_density = df_clean["Road_traffic_density"].unique()
    fig3, axes3 = plt.subplots(2, 2, figsize=(18,10))
    for ax, dens in zip(axes3.flatten(), traffic_density):
        traffic = df_clean[df_clean["Road_traffic_density"] == dens]
        sns.histplot(data=traffic, x="Time_taken (min)", kde=True, color="#5f6075", ax=ax)
        ax.set_title(f"{dens}")
        ax.set_xlabel("Time Taken (min)")
        ax.set_ylabel("Frequency")

    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=False)
    with st.expander("Insight"):
        st.markdown("""
1. **Jam**: Peak 25–35 min, wide range up to 55 min.  
2. **High**: Peak 25–30 min, range 20–40 min.  
3. **Medium**: Peak 25–30 min, range 20–35 min.  
4. **Low**: Peak 15–25 min, fastest and concentrated deliveries.
        """)


    # 4: Traffic & Weather Pattern Analysis
    st.markdown("## 4. Traffic & Weather Pattern Analysis")
    # Row 1: Traffic Distribution
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Road Traffic Density Distribution")
        fig1, ax1 = plt.subplots(figsize=(6,5))
        df_clean["Road_traffic_density"].value_counts().plot(kind='bar', ax=ax1, color="#5f6075")
        ax1.set_xlabel("Traffic Level")
        ax1.set_ylabel("Count")
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        st.pyplot(fig1, use_container_width=False)

    with col2:
        st.markdown("### Traffic Density Percentage")
        fig2, ax2 = plt.subplots(figsize=(4, 4))
        colors_soft_blue = ["#5f6075", "#3c3c50", "#9e8c75", "#e4e4e4"]
        df_clean["Road_traffic_density"].value_counts().plot(
            kind='pie',
            autopct='%1.1f%%',
            ax=ax2,
            colors=colors_soft_blue
        )
        ax2.set_ylabel("")
        fig2.tight_layout()
        st.pyplot(fig2, use_container_width=False)

    with st.expander("Insight"): 
        st.markdown(""" 
    **Most Frequent (Highest Frequency)**: Low traffic density is the most frequently recorded, with more than 11,000 incidents (approximately 34.1% of the total data). **Least Frequent (Lowest Frequency)**: High traffic density is the least frequently recorded, with fewer than 4,000 incidents (only 9.8% of the total data). Other Conditions: Congestion (Jam) ranks second with just over 10,000 incidents (approximately 31.6%), followed by Medium conditions with approximately 8,000 incidents (approximately 24.5%). """)

    # Row 2: Weather Distribution
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Weather Conditions Distribution")
        fig3, ax3 = plt.subplots(figsize=(6,5))
        df_clean["Weather_conditions"].value_counts().plot(kind='bar', ax=ax3, color="#5f6075")
        ax3.set_xlabel("Weather Condition")
        ax3.set_ylabel("Count")
        ax3.tick_params(axis='x', rotation=45)
        fig3.tight_layout()
        st.pyplot(fig3, use_container_width=False)

    with col2:
        st.markdown("### Weather Conditions Percentage")
        fig4, ax4 = plt.subplots(figsize=(4,4)) 
        colors_soft_blue = ["#5f6075", "#3c3c50", "#9e8c75", "#e4e4e4", "#fcf7f6", "#667b8a"]
        df_clean["Weather_conditions"].value_counts().plot(
            kind='pie', autopct='%1.1f%%', ax=ax4, colors=colors_soft_blue
        )
        ax4.set_ylabel("")
        fig4.tight_layout()
        st.pyplot(fig4, use_container_width=False)

    with st.expander("Insight"):
        st.markdown("""
    A very balanced number of observations for each weather condition. This means that the analysis of delivery times based on weather will not be biased due to the dominance of a particular weather condition in the dataset.
        """)

    
    # 5. Cluster-Based Operational Recommendations
    st.markdown("## 💡 Cluster-Based Operational Recommendations")

    st.markdown("""
Below are actionable recommendations derived from the K-Means geospatial clustering analysis.  
""")

    # Create Recommendation Table
    rec_data = {
        "Cluster": [
            "Cluster 0 – West-Central (Fog)",
            "Cluster 1 – South-Central (Stormy)",
            "Cluster 2 – East Region (Sandstorms)"
        ],
        "Key Characteristics": [
            "High-density area (19k+), foggy weather, low traffic",
            "Large region (16k+), stormy weather, low traffic",
            "Smallest region (4k), sandstorms, scattered geography"
        ],
        "Challenges": [
            "Fog reduces visibility, potential delays",
            "Storms increase travel risk and create unpredictable delays",
            "Longer distances & sandstorm disruptions"
        ],
        "Operational Recommendations": [
            "- Position riders near high-demand zones\n- Apply time-based route optimization\n- SLA remains stable due to low traffic",
            "- Add SLA buffer during storm periods\n- Enable real-time weather alerts\n- Prioritize safer route choices",
            "- Use extended SLA for remote deliveries\n- Add extra fleet coverage\n- Use demand heatmaps to optimize routing"
        ]
    }

    rec_df = pd.DataFrame(rec_data)

    st.dataframe(rec_df, use_container_width=True)

    st.markdown("""
### 💡 Summary  
- **Cluster 0** is the operational core — stable, low traffic, but fog requires visibility-aware routing.  
- **Cluster 1** needs **weather-based SLA adjustments** and **storm alerts** for safety.  
- **Cluster 2** requires **extra fleet scaling** and **flexible scheduling** due to distance and sandstorms.

These recommendations help optimize distances, cost, and SLA reliability.
""")

    
