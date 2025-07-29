import streamlit as st

import pandas as pd

import plotly.express as px

import os

import warnings



st.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

warnings.filterwarnings("ignore") # Moved this line after st.set_page_config()

st.title(" :bar_chart: Sales Dashboard")

st.markdown(

"<style>div.block-container{padding-top:2rem;} </style>", unsafe_allow_html=True

)



# File uploader

fl = st.file_uploader(

" :file_folder: Please upload a file", type=(["csv", "xlsx", "xls", "txt"])

)



# Function to read the file

def read_file(file_input):

df = None # Initialize df



# Determine if the input is an UploadedFile object or a string path

if hasattr(file_input, 'name') and hasattr(file_input, 'read'): # It's an UploadedFile object

file_name = file_input.name.lower()

source_for_pandas = file_input

elif isinstance(file_input, str): # It's a string path (though this path won't be used after modification)

file_name = file_input.lower()

source_for_pandas = file_input

else:

st.error("Invalid file input type provided to read_file function.")

return None



if file_name.endswith(".csv") or file_name.endswith(".txt"):

try:

df = pd.read_csv(source_for_pandas, encoding="ISO-8859-1")

except Exception as e:

st.error(f"Error reading CSV/TXT file: {e}")

st.exception(e)

elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):

try:

df = pd.read_excel(source_for_pandas)

except Exception as e:

st.error(f"Error reading Excel file: {e}")

st.exception(e)

else:

st.error("Unsupported file format. Please upload a CSV, TXT, XLS, or XLSX file.")



return df



# Check if file is uploaded, otherwise set df to None

if fl is not None:

filename = fl.name

st.write("Uploaded file:", filename)

df = read_file(fl) # Pass the UploadedFile object

else:

df = None # If no file is uploaded, df remains None



# Stop execution if no dataframe is available

if df is None:

st.warning("Please upload a data file to view the dashboard.")

st.stop()



# Ensure 'Order Date' is datetime

df["Order Date"] = pd.to_datetime(df["Order Date"])



# Date range filter

startDate = df["Order Date"].min()

endDate = df["Order Date"].max()



with st.sidebar:

st.header("Choose your filter:")

date1 = pd.to_datetime(st.date_input("Start Date", startDate))

date2 = pd.to_datetime(st.date_input("End Date", endDate))



# Apply date filter immediately

df_date_filtered = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()



# Region Filter

region = st.sidebar.multiselect("Pick your region", df_date_filtered["Region"].unique())

if not region:

df_region_filtered = df_date_filtered.copy()

else:

df_region_filtered = df_date_filtered[df_date_filtered["Region"].isin(region)]



# State Filter

state = st.sidebar.multiselect("Pick your state", df_region_filtered["State"].unique())

if not state:

df_state_filtered = df_region_filtered.copy()

else:

df_state_filtered = df_region_filtered[df_region_filtered["State"].isin(state)]



# City Filter

city = st.sidebar.multiselect("Pick your city", df_state_filtered["City"].unique())



# Final filtered DataFrame based on all selections

filtered_df = df_state_filtered.copy() # Start with the most filtered df (state)



if city:

filtered_df = filtered_df[filtered_df["City"].isin(city)]



# Check if filtered_df is empty after all filters

if filtered_df.empty:

st.warning("No data available for the selected filters. Please adjust your selections.")

st.stop() # Stop execution if no data



# --- Dashboard Visualizations ---

col1, col2 = st.columns((2))



# Category Wise Sales

category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()

with col1:

st.subheader("Category Wise Sales")

fig = px.bar(

category_df,

x="Category",

y="Sales",

text=[f"${x:,.2f}" for x in category_df["Sales"]],

template="seaborn",

)

st.plotly_chart(fig, use_container_width=True, height=200)



# Region Wise Sales

with col2:

st.subheader("Region Wise Sales")

fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)

fig.update_traces(text=filtered_df["Region"], textposition="outside")

st.plotly_chart(fig, use_container_width=True)



# Expanders for Category and Region Data

cl1, cl2 = st.columns((2))

with cl1:

with st.expander("Category_ViewData"):

st.write(category_df.style.background_gradient(cmap="Blues"))

csv = category_df.to_csv(index=False).encode("utf-8")

st.download_button(

"Download Data",

data=csv,

file_name="Category.csv",

mime="text/csv",

help="Click here to download",

)

with cl2:

with st.expander("Region_ViewData"): # Changed expander title for clarity

region_sales_df = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()

st.write(region_sales_df.style.background_gradient(cmap="Oranges"))

csv = region_sales_df.to_csv(index=False).encode("utf-8")

st.download_button(

"Download Data",

data=csv,

file_name="Region.csv",

mime="text/csv",

help="Click here to download",

)



# Time Series Analysis

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

"Download Data", data=csv, file_name="Timeseries.csv", mime="text/csv"

)



# Tree map based on region,category and sub-category

st.subheader("Hierarchical view of Sales using tree map.")

fig3 = px.treemap(

filtered_df,

path=["Region", "Category", "Sub-Category"],

values="Sales",

hover_data=["Sales"],

color="Sub-Category",

)

fig3.update_layout(width=800, height=650)

st.plotly_chart(fig3, use_container_width=True)



# Segment and Category wise Pie Charts

chart1, chart2 = st.columns((2))

with chart1:

st.subheader("Segment wise Sales")

fig = px.pie(filtered_df, values="Sales", names="Segment", template="plotly_dark")

fig.update_traces(text=filtered_df["Segment"], textposition="inside")

st.plotly_chart(fig, use_container_width=True)



with chart2:

st.subheader("Category wise Sales")

fig = px.pie(filtered_df, values="Sales", names="Category", template="gridon")

fig.update_traces(text=filtered_df["Category"], textposition="inside")

st.plotly_chart(fig, use_container_width=True)



# Month wise Sub-Category Sales Summary Table

import plotly.figure_factory as ff



st.subheader(" :point_right: Month wise Sub-Category Sales Summary")

with st.expander("Summary Table"):

# Displaying a sample of the original df for general summary

df_sample = df.head(5)[

["Region", "State", "City", "Category", "Sales", "Profit", "Quantity"]

]

fig = ff.create_table(df_sample, colorscale="Cividis")

st.plotly_chart(fig, use_container_width=True)



st.markdown("Month wise sub-category table")

# Ensure 'month' column is created on filtered_df for this table

filtered_df["month"] = filtered_df["Order Date"].dt.month_name()

sub_category_Year = pd.pivot_table(

data=filtered_df, values="Sales", index=["Sub-Category"], columns="month"

)

st.write(sub_category_Year.style.background_gradient(cmap="Blues"))



# Scatter plot

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

"x": 0.5, # Center the title

"xanchor": "center",

"yanchor": "top",

"font": dict(size=20),

},

xaxis=dict(title=dict(text="Sales", font=dict(size=19)), tickfont=dict(size=14)),

yaxis=dict(title=dict(text="Profit", font=dict(size=19)), tickfont=dict(size=14)),

)

st.plotly_chart(data1, use_container_width=True)



with st.expander("View Data (Filtered)"): # Changed title for clarity

st.write(filtered_df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges")).
