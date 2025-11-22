# pages/dashboard.py
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
import numpy as np
import os

# CACHE DATA & PREPROCESSING (FAST & MEMORY SAFE)
@st.cache_data
def load_dataset():
    """Load dataset once & reuse it (cache)."""
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "..", "data", "clustering_zomato.csv")
    df = pd.read_csv(data_path)
    return df


@st.cache_data
def compute_distance(df):
    """Precompute Haversine distances and return cached df."""
    
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        phi1, phi2 = np.radians(lat1), np.radians(lat2)
        dphi = np.radians(lat2 - lat1)
        dlambda = np.radians(lon2 - lon1)
        a = (
            np.sin(dphi/2)**2 +
            np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
        )
        return 2 * R * np.arcsin(np.sqrt(a))

    df["distance_km"] = haversine(
        df["Restaurant_latitude"],
        df["Restaurant_longitude"],
        df["Delivery_location_latitude"],
        df["Delivery_location_longitude"]
    )
    return df


# Load + preprocess
df_clean = compute_distance(load_dataset())

# Global color palette
base_color = "#5f6075"
custom_cmap = mcolors.LinearSegmentedColormap.from_list(
    "custom_map",
    ["#d6d7de", "#a3a4b3", base_color],
    N=256
)

# DASHBOARD PAGE
def dashboard_page():
    st.title("📊 Zomato Delivery Dashboard")

    # 1. GEOSPATIAL ANALYSIS
    st.markdown("## 1. Geospatial Distribution Analysis")
    col1, col2 = st.columns(2)

    # Scatter Plot
    with col1:
        st.markdown("### Customer Delivery Locations")
        fig, ax = plt.subplots(figsize=(6,5))
        ax.scatter(
            df_clean['Delivery_location_longitude'],
            df_clean['Delivery_location_latitude'],
            s=5, alpha=0.4, color=base_color
        )
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Customer Delivery Locations")
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"):
            st.markdown("""
The scatter plot shows customer delivery points concentrated mainly around longitude 73–76 and latitude 18–22, forming several dense clusters.
""")

    # Heatmap
    with col2:
        st.markdown("### Delivery Density Heatmap")
        fig, ax = plt.subplots(figsize=(6,5))
        sns.kdeplot(
            x=df_clean['Delivery_location_longitude'],
            y=df_clean['Delivery_location_latitude'],
            cmap=custom_cmap,
            fill=True,
            bw_method=0.3,
            alpha=0.8,
            ax=ax
        )
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_title("Delivery Density Heatmap")
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"):
            st.markdown("""
High-density areas appear around longitude 72–76 and latitude 18–22, indicating major customer hotspots.
""")

    # 2. Distance Analysis
    st.markdown("## 2. Distance Analysis")

    col1, col2 = st.columns(2)

    # -------------------------------
    # Distance Distribution (Histogram)
    # -------------------------------
    with col1:
        st.markdown("### Distribution of Delivery Distance")

        distance_counts = (
            df_clean['distance_km']
            .round()
            .value_counts()
            .sort_index()
        )

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.bar(distance_counts.index, distance_counts.values, color=base_color)
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Frequency")
        ax.set_title("Delivery Distance Distribution")
        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # -------------------------------
        # Insight
        # -------------------------------
        with st.expander("Insight"):
            st.markdown("""
            The histogram shows a fairly spread distribution of delivery distances, ranging from around **2 km to more than 20 km**, 
            with most deliveries falling within the **5–15 km range**.
            """)

    # -------------------------------
    # Distance vs Time
    # -------------------------------
    with col2:
        st.markdown("### Distance vs Delivery Time")

        fig, ax = plt.subplots(figsize=(6, 5))
        ax.scatter(df_clean["distance_km"], df_clean["Time_taken (min)"], alpha=0.6, color=base_color)
        ax.set_xlabel("Distance (km)")
        ax.set_ylabel("Delivery Time (min)")
        ax.set_title("Distance vs Delivery Time")
        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"):
            st.markdown("""
            The scatter plot shows the relationship between delivery distance and delivery time, where it generally appears that the greater 
            the distance, the greater the variation in delivery time, but there is no strong linear pattern. The data points are scattered 
            quite widely in each distance category, indicating that delivery time is influenced not only by distance but also by other 
            factors such as traffic conditions, routes, or courier efficiency. Although there is a slight tendency for delivery time to increase 
            with greater distance, the spread remains high, so the relationship between the variables can be said to be weak and inconsistent.
            """)

    # 3. DELIVERY TIME & DELAY ANALYSIS
    st.markdown("## 3. Delivery Time & Delay Analysis")
    col1, col2 = st.columns(2)

    # Time Taken Distribution
    with col1:
        st.markdown("### Distribution of Time Taken")
        time_counts = df_clean["Time_taken (min)"].round().value_counts().sort_index()
        fig, ax = plt.subplots(figsize=(6,5))
        ax.bar(time_counts.index, time_counts.values, color=base_color)
        ax.set_xlabel("Time Taken (min)")
        ax.set_ylabel("Frequency")
        ax.set_title("Delivery Time Distribution")
        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"): 
            st.markdown(""" 
The bar chart shows the distribution of time taken for delivery. The range of time taken is between 10 and 60 minutes, with the majority of deliveries taking between 15 and 30 minutes. 
        """)

    # Time by Weather
    with col2:
        st.markdown("### Delivery Time by Weather Conditions")
        unique_weather = df_clean["Weather_conditions"].unique()
        palette = {w: base_color for w in unique_weather}

        fig, ax = plt.subplots(figsize=(6,5))
        sns.boxplot(
            data=df_clean,
            x="Weather_conditions",
            y="Time_taken (min)",
            palette=palette,
            ax=ax
        )
        ax.set_title("Delivery Time by Weather")
        ax.tick_params(axis='x', rotation=45)
        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"): 
            st.markdown(""" 
**Longest Delivery Time (Highest Median)**: Foggy and cloudy conditions show the longest median delivery time, around 30–35 minutes. 
**Fastest Delivery Time (Lowest Median)**: Sunny conditions have the fastest median delivery time (~18 minutes). 
**Variability & Outliers**: Stormy, Sandstorms, and Windy conditions have similar medians (25–30 mins), with outliers indicating extreme delays. 
        """)

    # Time by City
    st.markdown("### Time Taken by City")
    cities = df_clean["City"].unique()
    fig, axes = plt.subplots(1, len(cities), figsize=(6*len(cities), 5))

    if len(cities) == 1:
        axes = [axes]

    for ax, city in zip(axes, cities):
        city_data = df_clean[df_clean["City"] == city]
        sns.histplot(city_data["Time_taken (min)"], kde=True, color=base_color, ax=ax)
        ax.set_title(city)
        ax.set_xlabel("Time Taken (min)")
    
    st.pyplot(fig)
    plt.close(fig)

    with st.expander("Insight"):
        st.markdown(""" 
         1. **Metropolitan**: Most deliveries 20–35 min, relatively stable despite high volume. 
         2. **Urban**: Faster deliveries 10–20 min, but long tail up to 50 min. 
         3. **Semi-Urban**: Slower 44–54 min but consistent, smaller dataset. 
    """)

    # 4. TRAFFIC & WEATHER PATTERNS
    st.markdown("## 4. Traffic & Weather Pattern Analysis")

    col1, col2 = st.columns(2)

    # Traffic Bar
    with col1:
        st.markdown("### Road Traffic Density Distribution")
        fig, ax = plt.subplots(figsize=(6,5))
        df_clean["Road_traffic_density"].value_counts().plot(kind='bar', color=base_color, ax=ax)
        ax.set_xlabel("Traffic Level")
        ax.set_ylabel("Count")
        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"):
            st.markdown(""" 
1. **Jam**: Peak 25–35 min, wide range up to 55 min. 
2. **High**: Peak 25–30 min, range 20–40 min. 
3. **Medium**: Peak 25–30 min, range 20–35 min. 
4. **Low**: Peak 15–25 min, fastest and concentrated deliveries. 
        """)

    # Traffic Pie
    with col2:
        st.markdown("### Traffic Density Percentage")
        fig, ax = plt.subplots(figsize=(3,3))
        df_clean["Road_traffic_density"].value_counts().plot(
            kind='pie', autopct='%1.1f%%', colors=["#5f6075", "#3c3c50", "#9e8c75", "#e4e4e4"], ax=ax
        )
        ax.set_ylabel("")
        fig.subplots_adjust(top=0.92)
        st.pyplot(fig)
        plt.close(fig)

        with st.expander("Insight"): 
            st.markdown(""" 
**Most Frequent (Highest Frequency)**: Low traffic density is the most frequently recorded, with more than 11,000 incidents (approximately 34.1% of the total data). 
**Least Frequent (Lowest Frequency)**: High traffic density is the least frequently recorded, with fewer than 4,000 incidents (only 9.8% of the total data). 
Other Conditions: Congestion (Jam) ranks second with just over 10,000 incidents (approximately 31.6%), followed by Medium conditions with approximately 8,000 incidents (approximately 24.5%). 
    """)

    # Weather Distribution
    col1, col2 = st.columns(2)
    weather_counts = df_clean["Weather_conditions"].value_counts()
    colors_purple = ["#5f6075", "#3c3c50", "#9e8c75", "#e4e4e4", "#fcf7f6", "#667b8a"]
    colors_used = colors_purple[:len(weather_counts)]

    with col1:
        st.markdown("### Weather Conditions Distribution")
        fig, ax = plt.subplots(figsize=(6,5))
        weather_counts.plot(kind='bar', color=colors_used, ax=ax)
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        st.markdown("### Weather Conditions Percentage")
        fig, ax = plt.subplots(figsize=(4,4))
        weather_counts.plot(
            kind='pie',
            autopct='%1.1f%%',
            colors=colors_used,
            ax=ax
        )
        ax.set_ylabel("")
        fig.subplots_adjust(top=0.88)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    
    with st.expander("Insight"): 
        st.markdown(""" A very balanced number of observations for each weather condition. This means that the analysis of delivery times based on weather will not be biased due to the dominance of a particular weather condition in the dataset. """)

    # 5. OPERATIONAL RECOMMENDATIONS
    st.markdown("## 💡 Cluster-Based Operational Recommendations")

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
            "Storms increase travel risk, unpredictable delays",
            "Long distances & sandstorm disruptions"
        ],
        "Operational Recommendations": [
            "- Position riders in hotspots\n- Optimize routes\n- SLA stable due to low traffic",
            "- Add SLA buffer during storms\n- Real-time weather alerts\n- Safety-first routing",
            "- Extra fleet & flexible scheduling\n- Extended SLA\n- Optimize using heatmaps"
        ]
    }

    st.dataframe(pd.DataFrame(rec_data), use_container_width=True)

    st.markdown("""
### 💡 Summary

- **Cluster 0** is the operational core — stable, low traffic, but fog requires visibility-aware routing.
- **Cluster 1** needs **weather-based SLA adjustments** and **storm alerts** for safety.
- **Cluster 2** requires **extra fleet scaling** and **flexible scheduling** due to distance and sandstorms.

These recommendations help optimize distances, cost, and SLA reliability.
""")


