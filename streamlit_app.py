import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Swiggy Data Analysis")

uploaded_file = st.file_uploader("Upload your Swiggy CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV Uploaded Successfully")

    st.markdown("""
    ### 📊 Dataset Overview
    - **Total Entries:** {}
    - **Columns:** {}
    - **Cities:** {}
    """.format(len(df), len(df.columns), df['City'].nunique()))

    st.dataframe(df.head())

    # Visualizations
    st.markdown("### 📦 Price Distribution by City")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x='City', y='Price', data=df, ax=ax1)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    st.pyplot(fig1)

    st.markdown("### ⭐ Price vs Average Rating")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='Price', y='Avg ratings', data=df, ax=ax2)
    st.pyplot(fig2)

    st.markdown("### ⚠️ Outlier Detection")
    st.dataframe(df[df['Price'] == 0])
    st.dataframe(df[df['Price'] > 1300])

    st.markdown("### 💰 Average Price by Food Type")
    st.dataframe(df.groupby('Food type')['Price'].mean().sort_values(ascending=False).head(10))

    st.markdown("### 🌟 Top-Rated Restaurants by City")
    top_rated = df.sort_values(by='Avg ratings', ascending=False)[['Restaurant', 'City', 'Avg ratings', 'Price']].head(10)
    st.dataframe(top_rated)

    st.markdown("### 🍽️ Most Popular Cuisines")
    fig3, ax3 = plt.subplots()
    df['Food type'].value_counts().head(10).plot(kind='barh', ax=ax3)
    st.pyplot(fig3)

    st.markdown("### 🕒 Delivery Time vs Rating")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x='Delivery time', y='Avg ratings', data=df, ax=ax4)
    st.pyplot(fig4)

    st.markdown("### 🥗 Cuisine Popularity vs Average Rating")
    st.dataframe(df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10))

    st.markdown("### 🏙️ Top Cities by Restaurant Count")
    fig5, ax5 = plt.subplots()
    df['City'].value_counts().head(10).plot(kind='bar', ax=ax5)
    st.pyplot(fig5)

    st.markdown("### ⏱️ Price vs Delivery Time")
    fig6, ax6 = plt.subplots()
    sns.scatterplot(x='Price', y='Delivery time', data=df, ax=ax6)
    st.pyplot(fig6)

    st.markdown("### 🧾 Price Distribution for Top 5 Food Types")
    top_foods = df['Food type'].value_counts().head(5).index
    fig7, ax7 = plt.subplots()
    sns.boxplot(x='Food type', y='Price', data=df[df['Food type'].isin(top_foods)], ax=ax7)
    plt.xticks(rotation=45)
    st.pyplot(fig7)

    st.markdown("### 💸 Cheapest and Costliest Cities")
    city_price = df.groupby('City')['Price'].agg(['min', 'max', 'mean']).sort_values(by='mean', ascending=False).head(10)
    st.dataframe(city_price)

    st.markdown("### ⭐ Rating Distribution per Food Type")
    fig8, ax8 = plt.subplots()
    df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10).plot(kind='barh', ax=ax8)
    st.pyplot(fig8)

    st.markdown("### 👎 Low-Rated Restaurants (Rating < 3.0)")
    st.dataframe(df[df['Avg ratings'] < 3.0][['Restaurant', 'City', 'Avg ratings', 'Price']])

    if 'Area' in df.columns:
        st.markdown("### 🏘️ Average Price by Area")
        area_price = df.groupby('Area')['Price'].mean().sort_values(ascending=False)
        st.dataframe(area_price)

    # New Insights
    st.markdown("### 📊 Correlation Matrix")
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(df[['Price', 'Avg ratings', 'Delivery time']].corr(), annot=True, cmap='coolwarm', ax=ax_corr)
    st.pyplot(fig_corr)

    st.markdown("### 📈 Price vs Cuisine Count")
    df['Cuisine Count'] = df['Food type'].apply(lambda x: len(str(x).split(',')))
    fig_cc, ax_cc = plt.subplots()
    sns.boxplot(x='Cuisine Count', y='Price', data=df, ax=ax_cc)
    st.pyplot(fig_cc)

    st.markdown("### 🏙️ Cities with Highest Average Ratings")
    top_rating_cities = df.groupby('City')['Avg ratings'].mean().sort_values(ascending=False).head(10)
    st.dataframe(top_rating_cities)

    st.markdown("### 🕐 Delivery Time Distribution by City")
    fig_del_time, ax_del_time = plt.subplots(figsize=(10, 5))
    sns.boxplot(x='City', y='Delivery time', data=df, ax=ax_del_time)
    plt.xticks(rotation=45)
    st.pyplot(fig_del_time)

    st.markdown("### 🍱 Top 20 Food Types by Volume")
    st.bar_chart(df['Food type'].value_counts().head(20))

    st.markdown("### ⏳ Average Delivery Time by Food Type")
    delivery_by_food = df.groupby('Food type')['Delivery time'].mean().sort_values(ascending=False).head(10)
    st.dataframe(delivery_by_food)

    st.markdown("### 🔄 Food Type vs Average Rating")
    fig9, ax9 = plt.subplots(figsize=(10, 6))
    df.groupby('Food type')['Avg ratings'].mean().sort_values().plot(kind='barh', ax=ax9)
    st.pyplot(fig9)

    st.markdown("### 📉 Food Type vs Price Distribution")
    top_food_types = df['Food type'].value_counts().head(10).index
    fig10, ax10 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Price', y='Food type', data=df[df['Food type'].isin(top_food_types)], ax=ax10)
    st.pyplot(fig10)

    st.markdown("### 🧾 Cheapest Food Items")
    cheapest_items = df[df['Price'] > 0].sort_values(by='Price').head(10)
    st.dataframe(cheapest_items[['Restaurant', 'Food type', 'Price', 'City']])

    st.markdown("### 📊 Top 5 Food Types in Each City")
    top_cities = df['City'].value_counts().head(5).index
    subset = df[df['City'].isin(top_cities)]
    food_city_counts = pd.crosstab(subset['City'], subset['Food type'])
    food_city_counts = food_city_counts[top_food_types]
    fig12, ax12 = plt.subplots(figsize=(10, 6))
    food_city_counts.plot(kind='bar', stacked=True, ax=ax12)
    plt.title("Top 5 Food Types in Top 5 Cities")
    plt.xlabel("City")
    plt.ylabel("Count")
    st.pyplot(fig12)

    st.markdown("## 📌 Final Summary")
    st.markdown("""
    - 25+ outputs included (visualizations, tables, insights)
    - Exploratory analysis of price, delivery, ratings, cuisine, and city metrics
    - Ideal for Swiggy business strategy, restaurant insights, and food trend research
    """)

else:
    st.info("Please upload your Swiggy CSV file to begin analysis.")
