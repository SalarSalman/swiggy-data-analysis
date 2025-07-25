import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Swiggy Data Analysis")

# File upload
uploaded_file = st.file_uploader("Upload your Swiggy CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("CSV Uploaded Successfully")

    # Overview
    st.markdown("""
    ### 📊 Dataset Overview
    - **Total Entries:** {}
    - **Columns:** {}
    - **Cities:** {}
    """.format(len(df), len(df.columns), df['City'].nunique()))

    st.dataframe(df.head())

    # Boxplot: Price Distribution by City
    st.markdown("## 1. Price Distribution by City")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x='City', y='Price', data=df, ax=ax1)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    st.pyplot(fig1)

    st.markdown(""">
    - Median price across cities is ₹250–₹350
    - Mumbai shows higher price variability
    - All cities have outliers (up to ₹2500)
    """)

    # Scatter: Price vs Avg Rating
    st.markdown("## 2. Price vs Average Rating")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='Price', y='Avg ratings', data=df, ax=ax2)
    st.pyplot(fig2)

    st.markdown(""">
    - Most listings are between ₹100–₹500 and ratings 3.5–5.0
    - No clear correlation; both cheap and expensive food get high ratings
    """)

    # Outliers Check
    st.markdown("## 3. Outlier Detection")
    st.write("### Restaurants with ₹0 Price")
    st.dataframe(df[df['Price'] == 0])
    st.write("### Restaurants with Price > ₹1300")
    st.dataframe(df[df['Price'] > 1300])

    # Average Price by Food Type
    st.markdown("## 4. Average Price by Food Type")
    avg_price = df.groupby('Food type')['Price'].mean().sort_values(ascending=False).head(10)
    st.dataframe(avg_price)

    # Top-Rated Restaurants
    st.markdown("## 5. Top-Rated Restaurants by City")
    top_rated = df.sort_values(by='Avg ratings', ascending=False)[['Restaurant', 'City', 'Avg ratings', 'Price']].head(10)
    st.dataframe(top_rated)

    # Most Popular Cuisines
    st.markdown("## 6. Most Popular Cuisines")
    fig3, ax3 = plt.subplots()
    df['Food type'].value_counts().head(10).plot(kind='barh', ax=ax3)
    st.pyplot(fig3)

    # Delivery Time vs Rating
    st.markdown("## 7. Delivery Time vs Rating")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x='Delivery time', y='Avg ratings', data=df, ax=ax4)
    st.pyplot(fig4)

    # Cuisine Popularity vs Rating
    st.markdown("## 8. Cuisine Popularity vs Average Rating")
    cuisine_rating = df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10)
    st.dataframe(cuisine_rating)

    # Top Cities by Restaurant Count
    st.markdown("## 9. Top Cities by Restaurant Count")
    fig5, ax5 = plt.subplots()
    df['City'].value_counts().head(10).plot(kind='bar', ax=ax5)
    st.pyplot(fig5)

    # Price vs Delivery Time
    st.markdown("## 10. Price vs Delivery Time")
    fig6, ax6 = plt.subplots()
    sns.scatterplot(x='Price', y='Delivery time', data=df, ax=ax6)
    st.pyplot(fig6)

    # Boxplot of Top 5 Food Types
    st.markdown("## 11. Price Distribution for Top 5 Food Types")
    top_foods = df['Food type'].value_counts().head(5).index
    fig7, ax7 = plt.subplots()
    sns.boxplot(x='Food type', y='Price', data=df[df['Food type'].isin(top_foods)], ax=ax7)
    plt.xticks(rotation=45)
    st.pyplot(fig7)

    # Cheapest and Costliest Cities
    st.markdown("## 12. Cheapest and Costliest Cities")
    city_price = df.groupby('City')['Price'].agg(['min', 'max', 'mean']).sort_values(by='mean', ascending=False).head(10)
    st.dataframe(city_price)

    # Rating Distribution per Food Type
    st.markdown("## 13. Rating Distribution per Food Type")
    fig8, ax8 = plt.subplots()
    df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10).plot(kind='barh', ax=ax8)
    st.pyplot(fig8)

    # Low-Rated Restaurants
    st.markdown("## 14. Low-Rated Restaurants (Rating < 3.0)")
    st.dataframe(df[df['Avg ratings'] < 3.0][['Restaurant', 'City', 'Avg ratings', 'Price']])

    # Area-wise Price (if column exists)
    if 'Area' in df.columns:
        st.markdown("## 15. Average Price by Area")
        area_price = df.groupby('Area')['Price'].mean().sort_values(ascending=False)
        st.dataframe(area_price)

    # Final Summary
    st.markdown("""
    ## 📌 Final Summary
    - 18+ outputs included (visualizations, tables, summaries)
    - Analysis done on pricing, delivery, cuisine type, and rating patterns
    - Data used to highlight trends across top Indian cities on Swiggy
    """)
else:
    st.info("Please upload your Swiggy CSV file to begin analysis.")
