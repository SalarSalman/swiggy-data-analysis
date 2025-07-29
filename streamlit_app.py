import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import warnings

# Suppress warnings globally at the very beginning
warnings.filterwarnings("ignore")

# Set Streamlit page configuration
st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

st.title("📊 Sales Dashboard")
st.markdown(
    "<style>div.block-container{padding-top:2rem;} </style>", unsafe_allow_html=True
)

# --- File Uploader and Data Loading ---
fl = st.file_uploader(
    "📂 Please upload a file", type=(["csv", "xlsx", "xls", "txt"])
)

@st.cache_data # Cache the data loading function for performance
def read_file(file_input):
    """
    Reads the uploaded file into a pandas DataFrame.
    Supports CSV, TXT, XLS, and XLSX formats.
    """
    df = None
    file_name = file_input.name.lower()

    try:
        if file_name.endswith((".csv", ".txt")):
            df = pd.read_csv(file_input, encoding="ISO-8859-1")
        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(file_input)
        else:
            st.error("Unsupported file format. Please upload a CSV, TXT, XLS, or XLSX file.")
            return None
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.exception(e)
        return None
    return df

df = None
if fl is not None:
    st.write("Uploaded file:", fl.name)
    df = read_file(fl)
else:
    st.warning("Please upload a data file to view the dashboard.")
    st.stop() # Stop execution if no file is uploaded

# --- Data Preprocessing ---
# Ensure 'Order Date' is datetime
if 'Order Date' in df.columns:
    df["Order Date"] = pd.to_datetime(df["Order Date"])
else:
    st.error("Column 'Order Date' not found in the uploaded file. Please ensure your file has this column.")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("Choose your filter:")

# Date range filter
startDate = df["Order Date"].min()
endDate = df["Order Date"].max()

date1 = pd.to_datetime(st.sidebar.date_input("Start Date", startDate))
date2 = pd.to_datetime(st.sidebar.date_input("End Date", endDate))

# Apply date filter
df_date_filtered = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

# Region Filter
# Check if 'Region' column exists before filtering
if 'Region' in df_date_filtered.columns:
    region_options = df_date_filtered["Region"].unique()
    region = st.sidebar.multiselect("Pick your region", region_options)
    if not region:
        df_region_filtered = df_date_filtered.copy()
    else:
        df_region_filtered = df_date_filtered[df_date_filtered["Region"].isin(region)]
else:
    st.sidebar.warning("Region column not found. Skipping region filter.")
    df_region_filtered = df_date_filtered.copy() # Proceed without region filter

# State Filter
# Check if 'State' column exists before filtering
if 'State' in df_region_filtered.columns:
    state_options = df_region_filtered["State"].unique()
    state = st.sidebar.multiselect("Pick your state", state_options)
    if not state:
        df_state_filtered = df_region_filtered.copy()
    else:
        df_state_filtered = df_region_filtered[df_region_filtered["State"].isin(state)]
else:
    st.sidebar.warning("State column not found. Skipping state filter.")
    df_state_filtered = df_region_filtered.copy() # Proceed without state filter

# City Filter
# Check if 'City' column exists before filtering
if 'City' in df_state_filtered.columns:
    city_options = df_state_filtered["City"].unique()
    city = st.sidebar.multiselect("Pick your city", city_options)
    if not city:
        filtered_df = df_state_filtered.copy()
    else:
        filtered_df = df_state_filtered[df_state_filtered["City"].isin(city)]
else:
    st.sidebar.warning("City column not found. Skipping city filter.")
    filtered_df = df_state_filtered.copy() # Proceed without city filter

# Check if filtered_df is empty after all filters
if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your selections.")
    st.stop() # Stop execution if no data

# --- Dashboard Visualizations ---

col1, col2 = st.columns((2))

# Category Wise Sales
if 'Category' in filtered_df.columns and 'Sales' in filtered_df.columns:
    category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()
    with col1:
        st.subheader("Category Wise Sales")
        fig = px.bar(
            category_df,
            x="Category",
            y="Sales",
            text=[f"${x:,.2f}" for x in category_df["Sales"]],
            template="seaborn",
            height=350 # Adjusted height for better fit
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    with col1:
        st.warning("Category or Sales column not found for Category Wise Sales chart.")

# Region Wise Sales
if 'Region' in filtered_df.columns and 'Sales' in filtered_df.columns:
    with col2:
        st.subheader("Region Wise Sales")
        fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
        fig.update_traces(text=filtered_df["Region"], textposition="outside")
        st.plotly_chart(fig, use_container_width=True)
else:
    with col2:
        st.warning("Region or Sales column not found for Region Wise Sales chart.")

# Expanders for Category and Region Data
cl1, cl2 = st.columns((2))
with cl1:
    if 'Category' in filtered_df.columns and 'Sales' in filtered_df.columns:
        with st.expander("Category Data View"):
            st.write(category_df.style.background_gradient(cmap="Blues"))
            csv = category_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Category Data",
                data=csv,
                file_name="Category_Sales.csv",
                mime="text/csv",
                help="Click here to download category-wise sales data",
            )
    else:
        with st.expander("Category Data View"):
            st.info("Category or Sales column not available to display data.")

with cl2:
    if 'Region' in filtered_df.columns and 'Sales' in filtered_df.columns:
        with st.expander("Region Data View"):
            region_sales_df = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
            st.write(region_sales_df.style.background_gradient(cmap="Oranges"))
            csv = region_sales_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Region Data",
                data=csv,
                file_name="Region_Sales.csv",
                mime="text/csv",
                help="Click here to download region-wise sales data",
            )
    else:
        with st.expander("Region Data View"):
            st.info("Region or Sales column not available to display data.")

# Time Series Analysis
if 'Order Date' in filtered_df.columns and 'Sales' in filtered_df.columns:
    st.subheader("Time Series Analysis")
    # Create 'month_year' as a string directly on filtered_df
    filtered_df["month_year"] = filtered_df["Order Date"].dt.strftime("%Y : %b")

    linechart = filtered_df.groupby("month_year")["Sales"].sum().reset_index()

    # Convert 'month_year' back to datetime for proper chronological sorting
    linechart['sort_key'] = pd.to_datetime(linechart['month_year'], format='%Y : %b')
    linechart = linechart.sort_values(by='sort_key').drop(columns='sort_key')

    fig2 = px.line(
        linechart,
        x="month_year",
        y="Sales",
        labels={"Sales": "Amount"},
        height=500,
        width=1000,
        template="gridon",
    )
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("View Data For Time Series"):
        st.write(linechart.T.style.background_gradient(cmap="Blues"))
        csv = linechart.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Time Series Data", data=csv, file_name="Timeseries_Sales.csv", mime="text/csv"
        )
else:
    st.subheader("Time Series Analysis")
    st.warning("Order Date or Sales column not found for Time Series Analysis.")

# Treemap based on region, category, and sub-category
if all(col in filtered_df.columns for col in ['Region', 'Category', 'Sub-Category', 'Sales']):
    st.subheader("Hierarchical view of Sales using Treemap.")
    fig3 = px.treemap(
        filtered_df,
        path=["Region", "Category", "Sub-Category"],
        values="Sales",
        hover_data=["Sales"],
        color="Sub-Category",
    )
    fig3.update_layout(width=800, height=650)
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.subheader("Hierarchical view of Sales using Treemap.")
    st.warning("Required columns (Region, Category, Sub-Category, Sales) not found for Treemap.")

# Segment and Category wise Pie Charts
chart1, chart2 = st.columns((2))
with chart1:
    if 'Segment' in filtered_df.columns and 'Sales' in filtered_df.columns:
        st.subheader("Segment wise Sales")
        fig = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")
        fig.update_traces(text=filtered_df["Segment"], textposition="inside")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.subheader("Segment wise Sales")
        st.warning("Segment or Sales column not found for Segment wise Sales chart.")

with chart2:
    if 'Category' in filtered_df.columns and 'Sales' in filtered_df.columns:
        st.subheader("Category wise Sales")
        fig = px.pie(filtered_df, values="Sales", names="Category", template="gridon")
        fig.update_traces(text=filtered_df["Category"], textposition="inside")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.subheader("Category wise Sales")
        st.warning("Category or Sales column not found for Category wise Sales chart.")

# Month wise Sub-Category Sales Summary Table
st.subheader("👉 Month wise Sub-Category Sales Summary")
with st.expander("Summary Table (First 500 rows of Filtered Data)"):
    # Displaying a sample of the filtered_df for general summary
    # Check if columns exist before displaying
    display_cols = [col for col in ["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"] if col in filtered_df.columns]
    if display_cols:
        df_sample = filtered_df.head(500)[display_cols]
        fig = ff.create_table(df_sample, colorscale="Cividis")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No relevant columns found for the summary table.")


st.markdown("Month wise sub-category table")
if all(col in filtered_df.columns for col in ['Order Date', 'Sub-Category', 'Sales']):
    # Ensure 'month' column is created on filtered_df for this table
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(
        data=filtered_df, values="Sales", index=["Sub-Category"], columns="month"
    )
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))
else:
    st.warning("Required columns (Order Date, Sub-Category, Sales) not found for Month wise Sub-Category Sales Summary.")

# Scatter plot
if all(col in filtered_df.columns for col in ['Sales', 'Profit', 'Quantity']):
    data1 = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        size="Quantity",
        title="Relationship between Sales and Profit",
    )

    data1.update_layout(
        title={
            "text": "Relationship between Sales and Profit",
            "x": 0.5,  # Center the title
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=20),
        },
        xaxis=dict(title=dict(text="Sales", font=dict(size=19)), tickfont=dict(size=14)),
        yaxis=dict(title=dict(text="Profit", font=dict(size=19)), tickfont=dict(size=14)),
    )
    st.plotly_chart(data1, use_container_width=True)
else:
    st.warning("Required columns (Sales, Profit, Quantity) not found for Scatter Plot.")


with st.expander("View Filtered Raw Data (First 500 rows)"):
    # Removed the trailing dot and ensured columns exist before slicing
    display_cols_raw = [col for col in filtered_df.columns if filtered_df.columns.get_loc(col) % 2 == 1 and filtered_df.columns.get_loc(col) < 20]
    if display_cols_raw:
        st.write(filtered_df.iloc[:500, :][display_cols_raw].style.background_gradient(cmap="Oranges"))
    else:
        st.info("No relevant columns found to display raw data sample.")
