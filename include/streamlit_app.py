import streamlit as st
import psycopg2
import pandas as pd
import altair as alt

def get_tiki_data(query):
    try:
        conn = psycopg2.connect(
            database="airflow",  
            user="airflow",      
            password="airflow",  
            host="postgres",     
            port="5432"          
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

@st.cache_data
def load_data():
    query = """
    SELECT name, detail_cate, large_cate, price, sale_quantity, rating_star, rating_quantity 
    FROM tiki_data
    """
    return get_tiki_data(query)


tiki_df = load_data()

tiki_df["sale_quantity"] = pd.to_numeric(tiki_df["sale_quantity"], errors="coerce")
tiki_df["rating_star"] = pd.to_numeric(tiki_df["rating_star"], errors="coerce")
tiki_df["rating_quantity"] = pd.to_numeric(tiki_df["rating_quantity"], errors="coerce")

# ------------
# STREAMLIT UI
# ------------
st.title("Tiki Products Sales and Ratings Analysis")

st.sidebar.header("Filter Products")

search_query = st.sidebar.text_input("Search by product name")

large_cate_options = tiki_df["large_cate"].unique().tolist()
large_cate_filter = st.sidebar.selectbox("Filter by large category", ["All"] + large_cate_options)

if large_cate_filter != "All":
    detail_cate_options = tiki_df[tiki_df["large_cate"] == large_cate_filter]["detail_cate"].unique().tolist()
else:
    detail_cate_options = tiki_df["detail_cate"].unique().tolist()
detail_cate_filter = st.sidebar.selectbox("Filter by detail category", ["All"] + detail_cate_options)

filtered_df = tiki_df.copy()

if search_query:
    filtered_df = filtered_df[filtered_df["name"].str.contains(search_query, case=False, na=False)]

if large_cate_filter != "All":
    filtered_df = filtered_df[filtered_df["large_cate"] == large_cate_filter]

if detail_cate_filter != "All":
    filtered_df = filtered_df[filtered_df["detail_cate"] == detail_cate_filter]

st.subheader("Filtered Product Data Table")
st.dataframe(filtered_df, use_container_width=True)

st.subheader(f"Total Products: {len(filtered_df)}")
st.subheader(f"Total Sales Quantity: {filtered_df['sale_quantity'].sum()}")

st.subheader("Visualize Products")
metric = st.selectbox("Choose metric to visualize:", ["Products", "Rating"])

if metric == "Products":
    top_selling_df = filtered_df.sort_values(by="sale_quantity", ascending=False).head()
    
    if not top_selling_df.empty:
        max_sales_quantity = top_selling_df['sale_quantity'].max()
        
        sales_chart = alt.Chart(top_selling_df).mark_bar().encode(
            x=alt.X("sale_quantity", title="Sales Quantity", scale=alt.Scale(domain=[0, max_sales_quantity])),
            y=alt.Y("name", sort="-x", title="Product Name"),
            tooltip=["name", "sale_quantity"]
        ).properties(width=700, height=400)
        st.altair_chart(sales_chart, use_container_width=True)
    else:
        st.write("No products found for the selected filters.")

if metric == "Rating":
    top_rated_df = filtered_df.sort_values(by=["rating_star", "rating_quantity"], ascending=False).head()
    
    if not top_rated_df.empty:
        rating_chart = alt.Chart(top_rated_df).mark_bar().encode(
            x=alt.X("rating_star", title="Rating Stars", scale=alt.Scale(domain=[0, 5])),
            y=alt.Y("name", sort="-x", title="Product Name"),
            tooltip=["name", "rating_star", "rating_quantity"]
        ).properties(width=700, height=400)
        st.altair_chart(rating_chart, use_container_width=True)
    else:
        st.write("No products found for the selected filters.")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This app provides insights into the sales and ratings of Tiki products. 
        You can search for specific products in the data table, and filter by large or detail categories.
        """
    )
if st.sidebar.button('Refresh Data'):
    st.cache_data.clear()