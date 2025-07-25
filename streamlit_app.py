import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Swiggy Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("Swiggy Analysis")
st.sidebar.markdown("Upload dataset and navigate through sections below.")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload your Swiggy CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Dataset loaded: {} rows".format(len(df)))

    # Sidebar navigation
    section = st.sidebar.radio(
        "Select Section:",
        [
            "Overview",
            "Price & Ratings",
            "Cuisine & City Insights",
            "Correlations & Trends",
            "Outliers & Extremes",
            "Final Summary"
        ]
    )

    # Common metrics
    total_entries = len(df)
    total_columns = len(df.columns)
    total_cities = df['City'].nunique()

    if section == "Overview":
        st.header("📊 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Entries", total_entries)
        col2.metric("Columns", total_columns)
        col3.metric("Unique Cities", total_cities)
        st.dataframe(df.head())

    elif section == "Price & Ratings":
        st.header("💸 Price & Rating Analysis")
        with st.expander("📦 Price Distribution by City"):
            fig, ax = plt.subplots(figsize=(10,4))
            sns.boxplot(x='City', y='Price', data=df, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)
        with st.expander("⭐ Price vs Avg Rating"):
            fig, ax = plt.subplots(figsize=(10,4))
            sns.scatterplot(x='Price', y='Avg ratings', data=df, ax=ax)
            st.pyplot(fig)
        with st.expander("📈 Food Type vs Price"):
            top_foods = df['Food type'].value_counts().head(10).index
            fig, ax = plt.subplots(figsize=(10,4))
            sns.boxplot(x='Price', y='Food type', data=df[df['Food type'].isin(top_foods)], ax=ax)
            st.pyplot(fig)

    elif section == "Cuisine & City Insights":
        st.header("🍽️ Cuisine and City Insights")
        with st.expander("🌟 Top-Rated Restaurants"):
            st.dataframe(df[df['Avg ratings']>=4.5][['Restaurant','City','Avg ratings','Price']].head(10))
        with st.expander("🍱 Top Food Types by Volume"):
            st.bar_chart(df['Food type'].value_counts().head(20))
        with st.expander("🏙️ Top Cities by Restaurant Count"):
            fig, ax = plt.subplots(figsize=(8,3))
            df['City'].value_counts().head(10).plot(kind='bar', ax=ax)
            ax.set_ylabel('Count')
            st.pyplot(fig)
        if 'Area' in df.columns:
            with st.expander("🏘️ Average Price by Area"):
                st.dataframe(df.groupby('Area')['Price'].mean().sort_values(ascending=False))

    elif section == "Correlations & Trends":
        st.header("🔄 Correlations & Trends")
        with st.expander("📊 Correlation Matrix"):
            fig, ax = plt.subplots(figsize=(6,4))
            sns.heatmap(df[['Price','Avg ratings','Delivery time']].corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        with st.expander("📈 Price vs Cuisine Count"):
            df['Cuisine Count'] = df['Food type'].apply(lambda x: len(str(x).split(',')))
            fig, ax = plt.subplots(figsize=(8,4))
            sns.boxplot(x='Cuisine Count', y='Price', data=df, ax=ax)
            st.pyplot(fig)
        with st.expander("🕐 Delivery Time Distribution by City"):
            fig, ax = plt.subplots(figsize=(8,4))
            sns.boxplot(x='City', y='Delivery time', data=df, ax=ax)
            ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
            st.pyplot(fig)

    elif section == "Outliers & Extremes":
        st.header("⚠️ Outliers & Extremes")
        with st.expander("🍽️ Cheapest Food Items"):
            cheapest = df[df['Price']>0].nsmallest(10,'Price')
            st.dataframe(cheapest[['Restaurant','Food type','Price','City']])
        with st.expander("💰 Costliest Food Items"):
            costliest = df.nlargest(10,'Price')
            st.dataframe(costliest[['Restaurant','Food type','Price','City']])

    elif section == "Final Summary":
        st.header("📌 Final Summary")
        st.markdown("""
        - Comprehensive insights across price, ratings, delivery, cuisine, and city metrics.  
        - Easily navigate sections via sidebar.  
        - Interactive expanders keep UI uncluttered.  
        - Ready for stakeholder presentations and strategic decision-making.
        """)

else:
    st.title("Welcome to the Swiggy Data Analysis App")
    st.write("Please upload your Swiggy CSV file using the sidebar to begin analysis.")
