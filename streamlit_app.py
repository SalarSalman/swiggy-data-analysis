
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set a wide layout and add a page title and icon
st.set_page_config(layout="wide", page_title="Swiggy Data Analysis Dashboard", page_icon="🍔")

# Custom CSS for a clean look
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .block-container {
        padding: 2rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #d6336c;
    }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Swiggy Data Analysis Dashboard")

# Sidebar for File Upload
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload your Swiggy CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ CSV Uploaded Successfully")

    # Dataset Overview
    st.markdown("""
    ## 🔍 Dataset Overview
    """)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Entries", len(df))
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Unique Cities", df['City'].nunique())

    with st.expander("📄 View Sample Data"):
        st.dataframe(df.head())

    # Visualizations
    st.markdown("## 📊 Visual Insights")

    # Original visualizations (using matplotlib/seaborn)
    with st.expander("1. 📦 Price Distribution by City"):
        fig1, ax1 = plt.subplots()
        sns.boxplot(x='City', y='Price', data=df, ax=ax1)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        st.pyplot(fig1)

    with st.expander("2. ⭐ Price vs Average Rating"):
        # Using Plotly for an interactive scatter plot
        fig_plotly_scatter = px.scatter(df, x='Price', y='Avg ratings', color='City',
                                        title='Price vs. Average Rating',
                                        hover_data=['Restaurant'])
        st.plotly_chart(fig_plotly_scatter, use_container_width=True)

    with st.expander("3. ⚠️ Outlier Detection"):
        st.write("### Restaurants with ₹0 Price")
        st.dataframe(df[df['Price'] == 0])
        st.write("### Restaurants with Price > ₹1300")
        st.dataframe(df[df['Price'] > 1300])

    with st.expander("4. 💰 Average Price by Food Type"):
        st.dataframe(df.groupby('Food type')['Price'].mean().sort_values(ascending=False).head(10))

    with st.expander("5. 🌟 Top-Rated Restaurants by City"):
        st.dataframe(df.sort_values(by='Avg ratings', ascending=False)[['Restaurant', 'City', 'Avg ratings', 'Price']].head(10))

    with st.expander("6. 🍽️ Most Popular Cuisines"):
        # Using st.bar_chart for a clean, simple visualization
        st.bar_chart(df['Food type'].value_counts().head(10))

    with st.expander("7. 🕒 Delivery Time vs Rating"):
        # Using Plotly for an interactive scatter plot
        fig_plotly_delivery = px.scatter(df, x='Delivery time', y='Avg ratings',
                                         title='Delivery Time vs. Average Rating',
                                         hover_data=['Restaurant', 'Food type'])
        st.plotly_chart(fig_plotly_delivery, use_container_width=True)

    with st.expander("8. 🥗 Cuisine Popularity vs Average Rating"):
        st.dataframe(df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10))

    with st.expander("9. 🏙️ Top Cities by Restaurant Count"):
        # Using st.bar_chart for a simple, good-looking bar chart
        st.bar_chart(df['City'].value_counts().head(10))

    with st.expander("10. ⏱️ Price vs Delivery Time"):
        # Using Plotly for an interactive scatter plot
        fig_plotly_price_delivery = px.scatter(df, x='Price', y='Delivery time',
                                               title='Price vs. Delivery Time',
                                               hover_data=['Restaurant'])
        st.plotly_chart(fig_plotly_price_delivery, use_container_width=True)

    with st.expander("11. 🧾 Price Distribution for Top 5 Food Types"):
        top_foods = df['Food type'].value_counts().head(5).index
        fig7, ax7 = plt.subplots()
        sns.boxplot(x='Food type', y='Price', data=df[df['Food type'].isin(top_foods)], ax=ax7)
        plt.xticks(rotation=45)
        st.pyplot(fig7)

    with st.expander("12. 💸 Cheapest and Costliest Cities"):
        st.dataframe(df.groupby('City')['Price'].agg(['min', 'max', 'mean']).sort_values(by='mean', ascending=False).head(10))

    with st.expander("13. ⭐ Rating Distribution per Food Type"):
        # Using st.bar_chart for a clean horizontal bar chart
        df_rating_by_food = df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10)
        st.bar_chart(df_rating_by_food)

    with st.expander("14. 👎 Low-Rated Restaurants (Rating < 3.0)"):
        st.dataframe(df[df['Avg ratings'] < 3.0][['Restaurant', 'City', 'Avg ratings', 'Price']])

    if 'Area' in df.columns:
        with st.expander("15. 🏘️ Average Price by Area"):
            st.dataframe(df.groupby('Area')['Price'].mean().sort_values(ascending=False))

    # --- New Analysis Sections from your request ---

    st.markdown("## 📊 Additional Visual Insights")

    with st.expander("16. Correlation Matrix"):
        st.markdown("### 16. Correlation Matrix")
        fig_corr, ax_corr = plt.subplots()
        sns.heatmap(df[['Price', 'Avg ratings', 'Delivery time']].corr(), annot=True, cmap='coolwarm', ax=ax_corr)
        st.pyplot(fig_corr)

    with st.expander("17. Price Trend by Cuisine Count"):
        st.markdown("### 17. Price vs Cuisine Count")
        # Ensure 'Cuisine Count' is calculated only once
        if 'Cuisine Count' not in df.columns:
            df['Cuisine Count'] = df['Food type'].apply(lambda x: len(str(x).split(',')) if isinstance(x, str) else 0)
        fig_cuisine_count, ax_cc = plt.subplots()
        sns.boxplot(x='Cuisine Count', y='Price', data=df, ax=ax_cc)
        st.pyplot(fig_cuisine_count)

    with st.expander("18. Top Cities with Highest Average Ratings"):
        st.markdown("### 18. Cities with Highest Average Ratings")
        top_rating_cities = df.groupby('City')['Avg ratings'].mean().sort_values(ascending=False).head(10)
        st.dataframe(top_rating_cities)
    
    with st.expander("19. Delivery Time Distribution by City"):
        st.markdown("### 19. Delivery Time Distribution by City")
        fig_del_time, ax_del_time = plt.subplots(figsize=(10, 5))
        sns.boxplot(x='City', y='Delivery time', data=df, ax=ax_del_time)
        plt.xticks(rotation=45)
        st.pyplot(fig_del_time)

    with st.expander("20. Top Food Types by Volume"):
        st.markdown("### 20. Top 20 Food Types by Volume")
        top_food_volume = df['Food type'].value_counts().head(20)
        st.bar_chart(top_food_volume)

    with st.expander("21. Average Delivery Time by Food Type"):
        st.markdown("### 21. Average Delivery Time by Food Type")
        delivery_by_food = df.groupby('Food type')['Delivery time'].mean().sort_values(ascending=False).head(10)
        st.dataframe(delivery_by_food)

    with st.expander("22. Food Type vs Average Rating (Bar Chart)"):
        st.markdown("### 22. Food Type vs Average Rating")
        df_rating_by_food_sorted = df.groupby('Food type')['Avg ratings'].mean().sort_values().head(10)
        fig9, ax9 = plt.subplots(figsize=(10, 6))
        df_rating_by_food_sorted.plot(kind='barh', ax=ax9)
        st.pyplot(fig9)

    with st.expander("23. Food Type vs Price Distribution (Box Plot)"):
        st.markdown("### 23. Food Type vs Price Distribution")
        top_food_types = df['Food type'].value_counts().head(10).index
        fig10, ax10 = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='Price', y='Food type', data=df[df['Food type'].isin(top_food_types)], ax=ax10)
        st.pyplot(fig10)

    with st.expander("24. Costliest Food Items"):
        st.markdown("### 24. Costliest Food Items (Top 10)")
        costliest_items = df[df['Price'] > 0].sort_values(by='Price', ascending=False).head(10)
        st.dataframe(costliest_items[['Restaurant', 'Food type', 'Price', 'City']])
    

    with st.expander("25. Top 5 Food Types in Each City (Stacked Bar)"):
        st.markdown("### 25. Top 5 Food Types in Each City")
        top_cities = df['City'].value_counts().head(5).index
        top_food_types = df['Food type'].value_counts().head(10).index
        subset = df[df['City'].isin(top_cities)]
        food_city_counts = pd.crosstab(subset['City'], subset['Food type'])
        
        common_food_types_in_top_cities = food_city_counts.sum(axis=0).sort_values(ascending=False).head(5).index
        food_city_counts = food_city_counts[common_food_types_in_top_cities]

        fig12, ax12 = plt.subplots(figsize=(10, 6))
        food_city_counts.plot(kind='bar', stacked=True, ax=ax12)
        plt.title("Top 5 Food Types in Top 5 Cities")
        plt.xlabel("City")
        plt.ylabel("Count")
        st.pyplot(fig12)

    # Summary
    st.markdown("""
    ## ✅ Final Summary
    - Over 25 visual and statistical insights generated
    - Covers pricing, rating, delivery, and cuisine trends
    - Based on restaurant data from Indian cities
    """)

else:
    st.info("📂 Please upload your Swiggy CSV file to begin analysis.")


