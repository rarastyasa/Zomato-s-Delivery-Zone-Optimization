# pages/home.py
import streamlit as st

def home_page():
    st.title("🛵 Zomato Delivery Zone Optimization")
    st.subheader("Making Deliveries Faster, Smarter, and More Efficient!")

    # Intro
    st.markdown("""
Welcome to the **Zomato Delivery Zone Optimization Project**!  
Ever wondered how food delivery operations can be optimized to save time and cost while keeping customers happy? 🍔🚴‍♂️

In this project, we explore how **geospatial clustering** can help Zomato create **optimized delivery zones** for faster and more consistent deliveries.  

You can check out the dataset used for this project [here](https://www.kaggle.com/datasets/saurabhbadole/zomato-delivery-operations-analytics-dataset) on Kaggle.
""")

    # Project Background
    st.markdown("## 📖 Project Background")
    st.markdown("""
Delivery efficiency is critical for Zomato. When orders are scattered across cities, drivers travel longer distances, leading to higher costs and inconsistent delivery times.  
By analyzing delivery locations with geospatial clustering, we can design **intelligent delivery zones** that optimize routes and improve service performance.
""")

    # Business Problem
    st.markdown("## ⚠️ Business Problem")
    st.markdown("""
Zomato currently faces several challenges in delivery operations:  
- **Longer delivery distances** → higher fuel and labor costs  
- **Inconsistent delivery times** → reduced customer satisfaction  

Our goal is to solve these problems using **data-driven delivery zone optimization**.
""")

    # Project Objectives
    st.markdown("## 🎯 Project Objectives")
    st.markdown("""
1. **Reduce delivery distances and operational costs** by clustering customer locations.  
2. **Improve delivery consistency** by designing zones that support predictable SLA.  
3. **Enable data-driven decision making** for assigning delivery zones and planning resources efficiently.  
""")

    st.markdown("""
✨ **Explore the tabs above to see clustering results, zone analysis, and SLA evaluation.**  
Let's dive into how data can transform Zomato's delivery operations! 🚀
""")
