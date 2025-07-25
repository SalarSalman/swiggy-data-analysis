import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Swiggy Data Analysis")

uploaded_file = st.file_uploader("Upload your Swiggy CSV", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Data Preview", df.head())

    st.write("### Price Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["Price"], bins=50, kde=True, ax=ax)
    st.pyplot(fig)

    st.write("### Boxplot by City")
    top_cities = df['City'].value_counts().head(5).index.tolist()
    filtered_df = df[df['City'].isin(top_cities)]
    fig2, ax2 = plt.subplots()
    sns.boxplot(data=filtered_df, x='City', y='Price', ax=ax2)
    st.pyplot(fig2)
