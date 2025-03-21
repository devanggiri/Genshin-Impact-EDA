# Genshin Impact Meta Guide: Play Smart, Touch Grass

**Overview**

This project is a statistical and machine learning-driven analysis of Genshin Impact’s character distribution, meta trends, and power scaling across multiple game versions. Using Exploratory Data Analysis (EDA), clustering techniques, and time-series forecasting, it provides strategic insights into the game’s evolving character meta.

**Key Insights**

* Character Distribution Trends: EDA on 100+ characters from Version 1.0 to the latest update, identifying statistical trends in character releases.
* Power Scaling: Ranked characters by raw ATK across ascension levels (20, 40, 60, 80, 90) and filtered by elemental affinity to identify meta units.
* Clustering Analysis: Applied K-Means, DBSCAN, and Hierarchical Clustering to categorize characters based on Vision, Region, Weapon Type, and Rarity.
* Time-Series Forecasting: Predicted future character release rates using ARIMA & Prophet, estimating an annual release pattern of ~10-12 characters per year.
* Statistical Region & Element Distribution:
    * Mondstadt, Liyue, and Inazuma have the highest character counts.
    * Pyro, Cryo, and Electro are the dominant elements.
* Weapon & Body Type Trends:
    * Swords are the most common weapon (~30%).
    * Medium female body types are the most frequently used (~29 characters).
* Deployed Interactive Web App: Built a Streamlit dashboard for real-time interactive analysis of character attributes, rarity, and release patterns.

**Technology & Tools**

* Python, Pandas, NumPy, Seaborn, Matplotlib – Data Cleaning & EDA
* Scikit-Learn (DBSCAN, K-Means, Hierarchical Clustering) – Character Clustering
* ARIMA, Prophet – Time Series Forecasting
* Streamlit – Deployed Web App for Interactive Analysis
* Jupyter Notebook – Data Exploration & Visualization
