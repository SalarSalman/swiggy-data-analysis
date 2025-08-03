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
    .st-emotion-cache-1r4qj8m {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🍽️ Swiggy Data Analysis Dashboard")

# --- Sidebar for File Upload and Filters ---
st.sidebar.header("📁 Upload & Filter Data")
uploaded_file = st.sidebar.file_uploader("Upload your Swiggy CSV", type="csv")

df = None
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ CSV Uploaded Successfully")

        # Create a copy for filtering to avoid modifying the original dataframe
        filtered_df = df.copy()

        # Interactive Filters
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔍 Filters")
        
        # Check if key columns exist before creating filters
        if 'City' in filtered_df.columns and 'Avg ratings' in filtered_df.columns and 'Price' in filtered_df.columns:
            city_options = st.sidebar.multiselect(
                "Select City",
                options=filtered_df['City'].unique(),
                default=filtered_df['City'].unique()
            )
            
            rating_range = st.sidebar.slider(
                "Select Rating Range",
                min_value=0.0,
                max_value=5.0,
                value=(filtered_df['Avg ratings'].min(), filtered_df['Avg ratings'].max()),
                step=0.1
            )
            
            price_max = int(filtered_df['Price'].max()) if 'Price' in filtered_df.columns and not filtered_df['Price'].isnull().all() else 1000
            price_range = st.sidebar.slider(
                "Select Price Range",
                min_value=0,
                max_value=price_max,
                value=(0, price_max)
            )
            
            # Filter the DataFrame based on user selections
            filtered_df = filtered_df[
                (filtered_df['City'].isin(city_options)) &
                (filtered_df['Avg ratings'] >= rating_range[0]) &
                (filtered_df['Avg ratings'] <= rating_range[1]) &
                (filtered_df['Price'] >= price_range[0]) &
                (filtered_df['Price'] <= price_range[1])
            ]
        else:
            st.warning("Uploaded file is missing required columns: 'City', 'Avg ratings', or 'Price'. Filtering will not be available.")
    except Exception as e:
        st.error(f"An error occurred while processing the CSV file: {e}")
        df = None
        filtered_df = pd.DataFrame()
else:
    st.info("📂 Please upload your Swiggy CSV file to begin analysis.")
    filtered_df = pd.DataFrame() # Create an empty DataFrame to avoid errors

# --- Main Dashboard Content ---
if not filtered_df.empty:
    st.header("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Restaurants", len(filtered_df))
    col2.metric("Unique Cities", filtered_df['City'].nunique())
    col3.metric("Average Rating", f"{filtered_df['Avg ratings'].mean():.2f} / 5")
    col4.metric("Average Price", f"₹ {filtered_df['Price'].mean():.2f}")

    with st.expander("📄 View Sample Data"):
        st.dataframe(filtered_df.head(10))

    st.markdown("---")
    
    # --- Dynamic Visualizations based on filtered_df ---
    st.header("Restaurant & Cuisine Analysis")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Price Distribution by City")
        fig1 = px.box(filtered_df, x='City', y='Price', color='City', title='Price Distribution by City')
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Top 10 Food Types by Volume")
        top_food_volume = filtered_df['Food type'].value_counts().head(10)
        fig_volume = px.bar(top_food_volume, x=top_food_volume.values, y=top_food_volume.index,
                            orientation='h', title='Most Popular Food Types')
        fig_volume.update_layout(xaxis_title="Count", yaxis_title="Food Type")
        st.plotly_chart(fig_volume, use_container_width=True)

    st.markdown("---")
    
    st.header("Rating & Delivery Insights")

    col_c, col_d = st.columns(2)
    with col_c:
        st.subheader("Price vs. Average Rating")
        fig_price_rating = px.scatter(filtered_df, x='Price', y='Avg ratings', color='City',
                                      title='Price vs. Average Rating', hover_data=['Restaurant', 'Food type'])
        st.plotly_chart(fig_price_rating, use_container_width=True)

    with col_d:
        st.subheader("Delivery Time Distribution by City")
        fig_del_time = px.box(filtered_df, x='City', y='Delivery time', color='City',
                              title='Delivery Time Distribution by City')
        st.plotly_chart(fig_del_time, use_container_width=True)
    
    st.markdown("---")

    with st.expander("More Detailed Analysis"):
        st.subheader("Correlation Heatmap")
        # Ensure the columns for correlation exist
        corr_df = filtered_df[['Price', 'Avg ratings', 'Delivery time']].dropna()
        if not corr_df.empty:
            fig_corr, ax_corr = plt.subplots()
            sns.heatmap(corr_df.corr(), annot=True, cmap='coolwarm', ax=ax_corr)
            st.pyplot(fig_corr)
        else:
            st.info("Insufficient data to calculate correlation.")

        st.subheader("Costliest and Cheapest Restaurants")
        costliest_items = filtered_df[filtered_df['Price'] > 0].sort_values(by='Price', ascending=False).head(10)
        cheapest_items = filtered_df[filtered_df['Price'] > 0].sort_values(by='Price', ascending=True).head(10)
        
        col_e, col_f = st.columns(2)
        with col_e:
            st.markdown("#### Costliest Restaurants")
            st.dataframe(costliest_items[['Restaurant', 'Food type', 'Price', 'City']])
        with col_f:
            st.markdown("#### Cheapest Restaurants")
            st.dataframe(cheapest_items[['Restaurant', 'Food type', 'Price', 'City']])

else:
    # Message to display when no file is uploaded or filter returns no data
    if uploaded_file is None:
        st.info("📂 Please upload your Swiggy CSV file to begin analysis.")
    elif uploaded_file is not None and df is not None and filtered_df.empty:
        st.warning("⚠️ No data matches the current filter settings. Please adjust the filters.")
