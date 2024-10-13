import streamlit as st
import psycopg2
import pandas as pd
import altair as alt

# PostgreSQL connection setup
def get_tiki_data(query):
    """Function to query PostgreSQL for Tiki data."""
    try:
        conn = psycopg2.connect(
            database="airflow",  # Your PostgreSQL database name
            user="airflow",      # Your PostgreSQL username
            password="airflow",  # Your PostgreSQL password
            host="postgres",     # Your PostgreSQL host
            port="5432"          # PostgreSQL port
        )
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        cursor.close()
        conn.close()

        return pd.DataFrame(rows, columns=columns)

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Retrieve the data
@st.cache_data
def load_data():
    query = "SELECT name, detail_cate, large_cate, price, sale_quantity, rating_star, rating_quantity FROM tiki_data"
    return get_tiki_data(query)


# Load data
tiki_df = load_data()  # Used for full dataset table

# ------------ #
# STREAMLIT UI #
# ------------ #

# Streamlit app title
st.title("Tiki Products Sales and Ratings Analysis")

# Sidebar: Filters
st.sidebar.header("Filter Products")

# Filter by product name
search_query = st.sidebar.text_input("Search by product name")

# Filter by large category (large_cate)
large_cate_options = tiki_df["large_cate"].unique().tolist()
large_cate_filter = st.sidebar.selectbox("Filter by large category", ["All"] + large_cate_options)

# Filter by detail category (detail_cate)
if large_cate_filter != "All":
    detail_cate_options = tiki_df[tiki_df["large_cate"] == large_cate_filter]["detail_cate"].unique().tolist()
else:
    detail_cate_options = tiki_df["detail_cate"].unique().tolist()
detail_cate_filter = st.sidebar.selectbox("Filter by detail category", ["All"] + detail_cate_options)

# Apply filters to the table data
filtered_df = tiki_df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]

if large_cate_filter != "All":
    filtered_df = filtered_df[filtered_df["large_cate"] == large_cate_filter]

if detail_cate_filter != "All":
    filtered_df = filtered_df[filtered_df["detail_cate"] == detail_cate_filter]

# Show the filtered table
st.subheader("Product Data Table")
st.dataframe(filtered_df, use_container_width=True)

# Charts Section (NOT affected by the search query in the table)
st.subheader(f"Total Products: {len(filtered_df)}")
st.subheader(f"Total Sales Quantity: {filtered_df['sale_quantity'].sum()}")
st.subheader("Best Selling")
metric = st.selectbox("Choose metric to visualize:", ["Products", "Rating"])

if metric == "Products":
    # Sort data by sales and limit to top 5 products
    top_selling_df = filtered_df.sort_values(by="sale_quantity", ascending=False).head(5)

    # Create a bar chart for top-selling products
    sales_chart = alt.Chart(top_selling_df).mark_bar().encode(
        x=alt.X("sale_quantity", title="Sales Quantity"),
        y=alt.Y("name", sort="-x", title="Product Name"),
        tooltip=["name", "sale_quantity"]
    ).properties(width=700, height=400)

    st.altair_chart(sales_chart, use_container_width=True)

if metric == "Rating":
    # Sort data by rating stars and rating quantity, then limit to top 5 products
    top_rated_df = filtered_df.sort_values(by=["rating_star", "rating_quantity"], ascending=False).head(5)

    # Create a bar chart for top-rated products
    rating_chart = alt.Chart(top_rated_df).mark_bar().encode(
        x=alt.X("rating_star", title="Rating Stars"),
        y=alt.Y("name", sort="-x", title="Product Name"),
        tooltip=["name", "rating_star", "rating_quantity"]
    ).properties(width=700, height=400)

    st.altair_chart(rating_chart, use_container_width=True)

# Sidebar for additional information
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This app provides insights into the sales and ratings of Tiki products. 
        You can search for specific products in the data table, and filter by large or detail categories.
        """
    )
    # st.button("Refresh Data")
