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
        st.markdown(""">
        - Median price across cities is ₹250–₹350
        - Mumbai shows higher price variability
        - All cities have outliers (up to ₹2500)
        """)

    with st.expander("2. ⭐ Price vs Average Rating"):
        fig_plotly_scatter = px.scatter(filtered_df, x='Price', y='Avg ratings', color='City',
                                        title='Price vs. Average Rating',
                                        hover_data=['Restaurant', 'Food type'],
                                        color_discrete_sequence=px.colors.qualitative.Plotly,
                                        template="plotly_dark")
        st.plotly_chart(fig_plotly_scatter, use_container_width=True)
        st.markdown(""">
        - Most listings are ₹100–₹500 with ratings 3.5–5.0
        - No strong correlation between price and rating
        """)

    with st.expander("3. ⚠ Outlier Detection"):
        st.subheader("Restaurants with ₹0 Price")
        st.dataframe(filtered_df[filtered_df['Price'] == 0])
        st.subheader("Restaurants with Price > ₹1300")
        st.dataframe(filtered_df[filtered_df['Price'] > 1300])

    with st.expander("4. 💰 Average Price by Food Type"):
        st.subheader("Average Price by Food Type (Top 10)")
        avg_price_by_food = filtered_df.groupby('Food type')['Price'].mean().sort_values(ascending=False).head(10)
        fig_avg_price = px.bar(avg_price_by_food, x=avg_price_by_food.index, y=avg_price_by_food.values,
                               title='Average Price by Food Type',
                               color=avg_price_by_food.values,
                               color_continuous_scale=px.colors.sequential.Plasma,
                               template="plotly_dark")
        fig_avg_price.update_layout(xaxis_title="Food Type", yaxis_title="Average Price")
        st.plotly_chart(fig_avg_price, use_container_width=True)

    with st.expander("5. 🌟 Top-Rated Restaurants by City"):
        st.subheader("Top-Rated Restaurants by Average Rating (Top 10)")
        st.dataframe(filtered_df.sort_values(by='Avg ratings', ascending=False)[['Restaurant', 'City', 'Avg ratings', 'Price']].head(10))

    with st.expander("6. 🍽 Most Popular Cuisines (Top 10)"):
        st.subheader("Most Popular Cuisines")
        top_food_volume = filtered_df['Food type'].value_counts().head(10)
        fig_volume = px.bar(top_food_volume, x=top_food_volume.values, y=top_food_volume.index,
                            orientation='h', title='Most Popular Food Types',
                            color_discrete_sequence=px.colors.qualitative.Vivid,
                            template="plotly_dark")
        fig_volume.update_layout(xaxis_title="Count", yaxis_title="Food Type")
        st.plotly_chart(fig_volume, use_container_width=True)

    with st.expander("7. 🕒 Delivery Time vs Rating"):
        fig4 = px.scatter(filtered_df, x='Delivery time', y='Avg ratings', color='City',
                          title='Delivery Time vs Rating',
                          color_discrete_sequence=px.colors.qualitative.T10,
                          template="plotly_dark")
        st.plotly_chart(fig4, use_container_width=True)

    with st.expander("8. 🥗 Cuisine Popularity vs Average Rating"):
        st.subheader("Average Rating for Popular Cuisines (Top 10)")
        cuisine_ratings = filtered_df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10)
        fig_cuisine_ratings = px.bar(cuisine_ratings, x=cuisine_ratings.values, y=cuisine_ratings.index,
                                     orientation='h', title='Average Rating for Popular Cuisines',
                                     color_discrete_sequence=px.colors.sequential.Blues, template="plotly_dark")
        fig_cuisine_ratings.update_layout(xaxis_title="Average Rating", yaxis_title="Food Type")
        st.plotly_chart(fig_cuisine_ratings, use_container_width=True)
        st.dataframe(cuisine_ratings)

    with st.expander("9. 🏙 Top Cities by Restaurant Count"):
        st.subheader("Top 10 Cities by Restaurant Count")
        city_counts = filtered_df['City'].value_counts().head(10)
        fig_city = px.bar(city_counts, x=city_counts.index, y=city_counts.values,
                          title='Top Cities by Restaurant Count',
                          color_discrete_sequence=px.colors.qualitative.Pastel,
                          template="plotly_dark")
        fig_city.update_layout(xaxis_title="City", yaxis_title="Count")
        st.plotly_chart(fig_city, use_container_width=True)

    with st.expander("10. ⏱ Price vs Delivery Time"):
        fig_plotly_price_delivery = px.scatter(filtered_df, x='Price', y='Delivery time', color='City',
                                               title='Price vs. Delivery Time',
                                               hover_data=['Restaurant'],
                                               color_discrete_sequence=px.colors.qualitative.T10,
                                               template="plotly_dark")
        st.plotly_chart(fig_plotly_price_delivery, use_container_width=True)

    with st.expander("11. 🧾 Price Distribution for Top 5 Food Types"):
        top_foods = filtered_df['Food type'].value_counts().head(5).index
        fig7 = px.box(filtered_df[filtered_df['Food type'].isin(top_foods)], x='Food type', y='Price', color='Food type',
                      title='Price Distribution for Top 5 Food Types',
                      color_discrete_sequence=px.colors.sequential.Sunset,
                      template="plotly_dark")
        st.plotly_chart(fig7, use_container_width=True)

    with st.expander("12. 💸 Cheapest and Costliest Cities"):
        st.subheader("Cheapest and Costliest Cities (by average price)")
        city_price_agg = filtered_df.groupby('City')['Price'].agg(['min', 'max', 'mean']).reset_index()
        fig_city_price = px.bar(city_price_agg.sort_values(by='mean', ascending=False), x='City', y='mean',
                                color='City', title='Cheapest and Costliest Cities by Average Price',
                                color_discrete_sequence=px.colors.qualitative.D3, template="plotly_dark")
        fig_city_price.update_layout(xaxis_title="City", yaxis_title="Average Price")
        st.plotly_chart(fig_city_price, use_container_width=True)
        st.dataframe(city_price_agg.sort_values(by='mean', ascending=False))

    with st.expander("13. ⭐ Rating Distribution per Food Type"):
        st.subheader("Average Rating Distribution per Food Type")
        fig8 = px.bar(filtered_df.groupby('Food type')['Avg ratings'].mean().sort_values(ascending=False).head(10),
                      orientation='h', title='Average Rating per Food Type',
                      color_discrete_sequence=px.colors.qualitative.Light24,
                      template="plotly_dark")
        st.plotly_chart(fig8, use_container_width=True)

    with st.expander("14. 👎 Low-Rated Restaurants (Rating < 3.0)"):
        st.subheader("Low-Rated Restaurants (Rating < 3.0)")
        st.dataframe(filtered_df[filtered_df['Avg ratings'] < 3.0][['Restaurant', 'City', 'Avg ratings', 'Price']])
    
    if 'Area' in filtered_df.columns:
        with st.expander("15. 🏘 Average Price by Area"):
            st.subheader("Average Price by Area")
            avg_price_by_area = filtered_df.groupby('Area')['Price'].mean().sort_values(ascending=False)
            fig_avg_area_price = px.bar(avg_price_by_area, x=avg_price_by_area.index, y=avg_price_by_area.values,
                                        title='Average Price by Area',
                                        color=avg_price_by_area.values,
                                        color_continuous_scale=px.colors.sequential.Viridis,
                                        template="plotly_dark")
            fig_avg_area_price.update_layout(xaxis_title="Area", yaxis_title="Average Price")
            st.plotly_chart(fig_avg_area_price, use_container_width=True)

    with st.expander("16. Correlation Matrix"):
        st.subheader("Correlation between Price, Rating, and Delivery Time")
        corr_df = filtered_df[['Price', 'Avg ratings', 'Delivery time']].dropna()
        if not corr_df.empty:
            fig_corr, ax_corr = plt.subplots(facecolor='#333333')
            sns.heatmap(corr_df.corr(), annot=True, cmap='viridis', ax=ax_corr)
            ax_corr.set_facecolor('#333333')
            plt.tick_params(colors='#e0e0e0')
            cbar = ax_corr.collections[0].colorbar
            cbar.ax.yaxis.set_tick_params(color='#e0e0e0')
            cbar.ax.yaxis.label.set_color('#e0e0e0')
            cbar.ax.tick_params(axis='y', colors='#e0e0e0')
            ax_corr.xaxis.label.set_color('#e0e0e0')
            ax_corr.yaxis.label.set_color('#e0e0e0')
            ax_corr.title.set_color('#FFD700')
            ax_corr.xaxis.set_tick_params(color='#e0e0e0')
            ax_corr.yaxis.set_tick_params(color='#e0e0e0')
            st.pyplot(fig_corr)
        else:
            st.info("Insufficient data to calculate correlation.")

    with st.expander("17. Price Trend by Cuisine Count"):
        st.subheader("Price vs Cuisine Count")
        filtered_df['Cuisine Count'] = filtered_df['Food type'].apply(lambda x: len(str(x).split(',')) if isinstance(x, str) else 0)
        fig_cuisine_count = px.box(filtered_df, x='Cuisine Count', y='Price', color='Cuisine Count',
                                   title='Price Distribution by Cuisine Count',
                                   color_discrete_sequence=px.colors.sequential.Plasma,
                                   template="plotly_dark")
        st.plotly_chart(fig_cuisine_count, use_container_width=True)

    with st.expander("18. Top Cities with Highest Average Ratings"):
        st.subheader("Top Cities with Highest Average Ratings")
        top_rating_cities = filtered_df.groupby('City')['Avg ratings'].mean().sort_values(ascending=False).head(10)
        fig_top_rating_cities = px.bar(top_rating_cities, x=top_rating_cities.index, y=top_rating_cities.values,
                                       title='Top Cities by Average Rating',
                                       color=top_rating_cities.values,
                                       color_continuous_scale=px.colors.sequential.Agsunset,
                                       template="plotly_dark")
        fig_top_rating_cities.update_layout(xaxis_title="City", yaxis_title="Average Rating")
        st.plotly_chart(fig_top_rating_cities, use_container_width=True)
        st.dataframe(top_rating_cities)

    with st.expander("19. Delivery Time Distribution by City"):
        st.subheader("Delivery Time Distribution by City")
        fig_del_time = px.box(filtered_df, x='City', y='Delivery time', color='City',
                              title='Delivery Time Distribution by City',
                              color_discrete_sequence=px.colors.qualitative.T10,
                              template="plotly_dark")
        st.plotly_chart(fig_del_time, use_container_width=True)

    with st.expander("20. Top Food Types by Volume"):
        st.subheader("Top 20 Food Types by Volume")
        top_food_volume = filtered_df['Food type'].value_counts().head(20)
        fig_volume_20 = px.bar(top_food_volume, x=top_food_volume.index, y=top_food_volume.values,
                               title='Top 20 Food Types by Volume',
                               color=top_food_volume.values,
                               color_continuous_scale=px.colors.sequential.Viridis,
                               template="plotly_dark")
        fig_volume_20.update_layout(xaxis_title="Food Type", yaxis_title="Count")
        st.plotly_chart(fig_volume_20, use_container_width=True)

    with st.expander("21. Average Delivery Time by Food Type"):
        st.subheader("Average Delivery Time by Food Type (Top 10)")
        delivery_by_food = filtered_df.groupby('Food type')['Delivery time'].mean().sort_values(ascending=False).head(10)
        fig_delivery_by_food = px.bar(delivery_by_food, x=delivery_by_food.index, y=delivery_by_food.values,
                                      title='Average Delivery Time by Food Type',
                                      color=delivery_by_food.values,
                                      color_continuous_scale=px.colors.sequential.Sunset,
                                      template="plotly_dark")
        fig_delivery_by_food.update_layout(xaxis_title="Food Type", yaxis_title="Average Delivery Time")
        st.plotly_chart(fig_delivery_by_food, use_container_width=True)
        st.dataframe(delivery_by_food)

    with st.expander("22. Food Type vs Average Rating (Bar Chart)"):
        st.subheader("Food Type vs Average Rating")
        fig9 = px.bar(filtered_df.groupby('Food type')['Avg ratings'].mean().sort_values().tail(10),
                      orientation='h', title='Top 10 Food Types by Average Rating',
                      color_discrete_sequence=px.colors.sequential.Rainbow,
                      template="plotly_dark")
        st.plotly_chart(fig9, use_container_width=True)

    with st.expander("23. Food Type vs Price Distribution (Box Plot)"):
        st.subheader("Price Distribution for Top 10 Food Types")
        top_food_types = filtered_df['Food type'].value_counts().head(10).index
        fig10 = px.box(filtered_df[filtered_df['Food type'].isin(top_food_types)], x='Price', y='Food type',
                       title='Price Distribution for Top 10 Food Types',
                       color='Food type',
                       color_discrete_sequence=px.colors.qualitative.G10,
                       template="plotly_dark")
        st.plotly_chart(fig10, use_container_width=True)

    with st.expander("24. Cheapest Food Items"):
        st.subheader("Cheapest Food Items (Top 10)")
        cheapest_items = filtered_df[filtered_df['Price'] > 0].sort_values(by='Price').head(10)
        st.dataframe(cheapest_items[['Restaurant', 'Food type', 'Price', 'City']])

    with st.expander("25. Top 5 Food Types in Each City (Stacked Bar)"):
        st.subheader("Top 5 Food Types in Each City")
        top_cities = filtered_df['City'].value_counts().head(5).index
        subset = filtered_df[filtered_df['City'].isin(top_cities)]
        food_city_counts = pd.crosstab(subset['City'], subset['Food type'])
        
        common_food_types_in_top_cities = food_city_counts.sum(axis=0).sort_values(ascending=False).head(5).index
        food_city_counts = food_city_counts[common_food_types_in_top_cities]

        fig12 = px.bar(food_city_counts.T, x=food_city_counts.T.index, y=food_city_counts.T.columns,
                       title="Top 5 Food Types in Top 5 Cities",
                       template="plotly_dark")
        fig12.update_layout(xaxis_title="Food Type", yaxis_title="Count")
        st.plotly_chart(fig12, use_container_width=True)

    # Summary
    st.markdown("""
    ## ✅ Final Summary
    - Over 25 visual and statistical insights generated
    - Covers pricing, rating, delivery, and cuisine trends
    - Based on restaurant data from Indian cities
    """)

else:
    st.info("📂 Please upload your Swiggy CSV file to begin analysis.")
