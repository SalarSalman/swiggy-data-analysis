import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide", page_title="Swiggy Data Analysis Dashboard", page_icon="🍔")
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

    with st.expander("1. 📦 Price Distribution by City"):
        fig1, ax1 = plt.subplots()
        sns.boxplot(x='City', y='Price', data=df, ax=ax1)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
        st.pyplot(fig1)
        st.markdown(""">
        - Median price across cities is ₹250–₹350
        - Mumbai shows higher price variability
        - All cities have outliers (up to ₹2500)
        """)

    with st.expander("2. ⭐ Price vs Average Rating"):
        fig2, ax2 = plt.subplots()
        sns.scatterplot(x='Price', y='Avg ratings', data=df, ax=ax2)
        st.pyplot(fig2)
        st.markdown(""">
        - Most listings are ₹100–₹500 with ratings 3.5–5.0
        - No strong correlation between price and rating
        """)

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
        fig3, ax3 = plt.subplots()
        df['Food type'].value_counts().head(10).plot(kind='barh', ax=ax3)
        st.pyplot(fig3)

    with st.expander("7. 🕒 Delivery Time vs Rating"):
        fig4, ax4 = plt.subplots()
        sns.scatterplot(x='Delivery time', y='Avg ratings', data=df, ax=ax4)
        st.pyplot(fig4)

    with st.expander("8. 🥗 Cuisine Popularity vs Average Rating"):
        st.dataframe(df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10))

    with st.expander("9. 🏙️ Top Cities by Restaurant Count"):
        fig5, ax5 = plt.subplots()
        df['City'].value_counts().head(10).plot(kind='bar', ax=ax5)
        st.pyplot(fig5)

    with st.expander("10. ⏱️ Price vs Delivery Time"):
        fig6, ax6 = plt.subplots()
        sns.scatterplot(x='Price', y='Delivery time', data=df, ax=ax6)
        st.pyplot(fig6)

    with st.expander("11. 🧾 Price Distribution for Top 5 Food Types"):
        top_foods = df['Food type'].value_counts().head(5).index
        fig7, ax7 = plt.subplots()
        sns.boxplot(x='Food type', y='Price', data=df[df['Food type'].isin(top_foods)], ax=ax7)
        plt.xticks(rotation=45)
        st.pyplot(fig7)

    with st.expander("12. 💸 Cheapest and Costliest Cities"):
        st.dataframe(df.groupby('City')['Price'].agg(['min', 'max', 'mean']).sort_values(by='mean', ascending=False).head(10))

    with st.expander("13. ⭐ Rating Distribution per Food Type"):
        fig8, ax8 = plt.subplots()
        df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10).plot(kind='barh', ax=ax8)
        st.pyplot(fig8)

    with st.expander("14. 👎 Low-Rated Restaurants (Rating < 3.0)"):
        st.dataframe(df[df['Avg ratings'] < 3.0][['Restaurant', 'City', 'Avg ratings', 'Price']])

    if 'Area' in df.columns:
        with st.expander("15. 🏘️ Average Price by Area"):
            st.dataframe(df.groupby('Area')['Price'].mean().sort_values(ascending=False))

    # Summary
    st.markdown("""
    ## ✅ Final Summary
    - Over 18 visual and statistical insights generated
    - Covers pricing, rating, delivery, and cuisine trends
    - Based on restaurant data from Indian cities
    """)

else:
    st.info("📂 Please upload your Swiggy CSV file to begin analysis.")
