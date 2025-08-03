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
        background-color: #212121; /* Dark grey background */
        color: #e0e0e0; /* Light text for contrast */
    }
    .st-emotion-cache-1c1l9q1 { /* Sidebar background */
        background-color: #333333;
        color: #e0e0e0;
    }
    .block-container {
        padding: 2rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FFD700; /* Gold color for headers */
    }
    .st-emotion-cache-1r4qj8m {
        background-color: #333333; /* Darker background for metrics and expanders */
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
    }
    /* Style for Streamlit dataframes */
    .stDataFrame {
        background-color: #424242;
        color: #e0e0e0;
        border-radius: 10px;
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

    with st.expander("📄 View Filtered Sample Data"):
        st.subheader("Filtered Sample Data")
        st.dataframe(filtered_df.head(10))

    st.markdown("---")
    
    # --- All Visualizations in a Linear Layout ---
    st.header("Visual Insights & Analysis")
    
    with st.expander("1. 📦 Price Distribution by City"):
        fig1 = px.box(filtered_df, x='City', y='Price', color='City', title='Price Distribution by City',
                      color_discrete_sequence=px.colors.sequential.Viridis,
                      template="plotly_dark")
        st.plotly_chart(fig1, use_container_width=True)

    with st.expander("2. ⭐ Price vs Average Rating"):
        fig_plotly_scatter = px.scatter(filtered_df, x='Price', y='Avg ratings', color='City',
                                        title='Price vs. Average Rating',
                                        hover_data=['Restaurant', 'Food type'],
                                        color_discrete_sequence=px.colors.qualitative.Plotly,
                                        template="plotly_dark")
        st.plotly_chart(fig_plotly_scatter, use_container_width=True)

    with st.expander("3. 🍽️ Most Popular Cuisines (Top 10)"):
        top_food_volume = filtered_df['Food type'].value_counts().head(10)
        fig_volume = px.bar(top_food_volume, x=top_food_volume.values, y=top_food_volume.index,
                            orientation='h', title='Most Popular Food Types',
                            color_discrete_sequence=px.colors.qualitative.Vivid,
                            template="plotly_dark")
        fig_volume.update_layout(xaxis_title="Count", yaxis_title="Food Type")
        st.plotly_chart(fig_volume, use_container_width=True)
        
    with st.expander("4. ⏱️ Price vs Delivery Time"):
        fig_plotly_price_delivery = px.scatter(filtered_df, x='Price', y='Delivery time', color='City',
                                               title='Price vs. Delivery Time',
                                               hover_data=['Restaurant'],
                                               color_discrete_sequence=px.colors.qualitative.T10,
                                               template="plotly_dark")
        st.plotly_chart(fig_plotly_price_delivery, use_container_width=True)

    with st.expander("5. 💸 Cheapest and Costliest Cities"):
        st.subheader("Cheapest and Costliest Cities (by average price)")
        city_price_agg = filtered_df.groupby('City')['Price'].agg(['min', 'max', 'mean']).reset_index()
        fig_city_price = px.bar(city_price_agg.sort_values(by='mean', ascending=False), x='City', y='mean',
                                color='City', title='Cheapest and Costliest Cities by Average Price',
                                color_discrete_sequence=px.colors.qualitative.D3, template="plotly_dark")
        fig_city_price.update_layout(xaxis_title="City", yaxis_title="Average Price")
        st.plotly_chart(fig_city_price, use_container_width=True)
        st.dataframe(city_price_agg.sort_values(by='mean', ascending=False))
        
    with st.expander("6. 🌟 Top-Rated Restaurants"):
        st.subheader("Top-Rated Restaurants by Average Rating (Top 10)")
        st.dataframe(filtered_df.sort_values(by='Avg ratings', ascending=False)[['Restaurant', 'City', 'Avg ratings', 'Price']].head(10))
        
    with st.expander("7. 👎 Low-Rated Restaurants (Rating < 3.0)"):
        st.subheader("Low-Rated Restaurants (Rating < 3.0)")
        st.dataframe(filtered_df[filtered_df['Avg ratings'] < 3.0][['Restaurant', 'City', 'Avg ratings', 'Price']])
    
    with st.expander("8. 🧾 Price Distribution for Top 5 Food Types"):
        top_foods = filtered_df['Food type'].value_counts().head(5).index
        fig7 = px.box(filtered_df[filtered_df['Food type'].isin(top_foods)], x='Food type', y='Price', color='Food type',
                      title='Price Distribution for Top 5 Food Types',
                      color_discrete_sequence=px.colors.sequential.Sunset,
                      template="plotly_dark")
        st.plotly_chart(fig7, use_container_width=True)
        
    with st.expander("9. 🏙️ Top Cities by Restaurant Count"):
        st.subheader("Top 10 Cities by Restaurant Count")
        city_counts = filtered_df['City'].value_counts().head(10)
        fig_city = px.bar(city_counts, x=city_counts.index, y=city_counts.values,
                          title='Top Cities by Restaurant Count',
                          color_discrete_sequence=px.colors.qualitative.Pastel,
                          template="plotly_dark")
        fig_city.update_layout(xaxis_title="City", yaxis_title="Count")
        st.plotly_chart(fig_city, use_container_width=True)

    with st.expander("10. 🥗 Cuisine Popularity vs Average Rating"):
        st.subheader("Average Rating for Popular Cuisines (Top 10)")
        cuisine_ratings = filtered_df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10)
        fig_cuisine_ratings = px.bar(cuisine_ratings, x=cuisine_ratings.values, y=cuisine_ratings.index,
                                     orientation='h', title='Average Rating for Popular Cuisines',
                                     color_discrete_sequence=px.colors.sequential.Blues, template="plotly_dark")
        fig_cuisine_ratings.update_layout(xaxis_title="Average Rating", yaxis_title="Food Type")
        st.plotly_chart(fig_cuisine_ratings, use_container_width=True)
        st.dataframe(cuisine_ratings)

    with st.expander("11. Correlation Matrix"):
        st.subheader("Correlation between Price, Rating, and Delivery Time")
        corr_df = filtered_df[['Price', 'Avg ratings', 'Delivery time']].dropna()
        if not corr_df.empty:
            # Create the matplotlib figure and axes
            fig_corr, ax_corr = plt.subplots(facecolor='#333333')
            # Create the heatmap without the invalid cbar_kws argument
            sns.heatmap(corr_df.corr(), annot=True, cmap='viridis', ax=ax_corr)
            # Set the facecolor and tick colors for the axes
            ax_corr.set_facecolor('#333333')
            plt.tick_params(colors='#e0e0e0')
            # Get the colorbar and set its tick colors
            cbar = ax_corr.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color='#e0e0e0')
            cbar.ax.yaxis.label.set_color('#e0e0e0')
            cbar.ax.tick_params(axis='y', colors='#e0e0e0')
            # Set the text color for the labels
            ax_corr.xaxis.label.set_color('#e0e0e0')
            ax_corr.yaxis.label.set_color('#e0e0e0')
            ax_corr.title.set_color('#FFD700')
            ax_corr.xaxis.set_tick_params(color='#e0e0e0')
            ax_corr.yaxis.set_tick_params(color='#e0e0e0')
            st.pyplot(fig_corr)
        else:
            st.info("Insufficient data to calculate correlation.")

    with st.expander("12. Costliest and Cheapest Restaurants"):
        st.subheader("Top 10 Costliest & Cheapest Restaurants")
        costliest_items = filtered_df[filtered_df['Price'] > 0].sort_values(by='Price', ascending=False).head(10)
        cheapest_items = filtered_df[filtered_df['Price'] > 0].sort_values(by='Price', ascending=True).head(10)
        
        st.markdown("#### Costliest Restaurants")
        st.dataframe(costliest_items[['Restaurant', 'Food type', 'Price', 'City']])
        
        st.markdown("#### Cheapest Restaurants")
        st.dataframe(cheapest_items[['Restaurant', 'Food type', 'Price', 'City']])
    
    # --- New Insights Added ---
    
    if 'Delivery time' in filtered_df.columns:
        with st.expander("13. ⏱️ Average Delivery Time by City"):
            st.subheader("Average Delivery Time by City")
            avg_delivery = filtered_df.groupby('City')['Delivery time'].mean().sort_values(ascending=False)
            fig_avg_del = px.bar(avg_delivery, x=avg_delivery.index, y=avg_delivery.values,
                                 title='Average Delivery Time by City',
                                 color_discrete_sequence=px.colors.sequential.Rainbow,
                                 template="plotly_dark")
            fig_avg_del.update_layout(xaxis_title="City", yaxis_title="Average Delivery Time (minutes)")
            st.plotly_chart(fig_avg_del, use_container_width=True)

    if 'Cuisine Count' not in filtered_df.columns and 'Food type' in filtered_df.columns:
        filtered_df['Cuisine Count'] = filtered_df['Food type'].apply(lambda x: len(str(x).split(',')) if isinstance(x, str) else 0)

    if 'Cuisine Count' in filtered_df.columns:
        with st.expander("14. 🍔 Price vs. Cuisine Count"):
            st.subheader("Price vs. Number of Cuisines Offered")
            fig_cuisine_count = px.box(filtered_df, x='Cuisine Count', y='Price', color='Cuisine Count',
                                       title='Price Distribution by Cuisine Count',
                                       color_discrete_sequence=px.colors.sequential.Plasma,
                                       template="plotly_dark")
            st.plotly_chart(fig_cuisine_count, use_container_width=True)

    if 'Ratings' in filtered_df.columns:
        with st.expander("15. 🌟 Top Restaurants by Number of Ratings"):
            st.subheader("Top Restaurants by Total Ratings (Top 10)")
            top_rated_restaurants = filtered_df.sort_values(by='Ratings', ascending=False).head(10)
            st.dataframe(top_rated_restaurants[['Restaurant', 'City', 'Avg ratings', 'Ratings', 'Price']])
    
    with st.expander("16. ⚠️ Restaurants with High/Low Price"):
        st.write("### Restaurants with ₹0 Price")
        st.dataframe(filtered_df[filtered_df['Price'] == 0])
        st.write("### Restaurants with Price > ₹1300")
        st.dataframe(filtered_df[filtered_df['Price'] > 1300])

else:
    # Message to display when no file is uploaded or filter returns no data
    if uploaded_file is None:
        st.info("📂 Please upload your Swiggy CSV file to begin analysis.")
    elif uploaded_file is not None and df is not None and filtered_df.empty:
        st.warning("⚠️ No data matches the current filter settings. Please adjust the filters.")
