import psycopg2
import pandas as pd

def load_tiki_data():
    print("Load Tiki data...")
    # Thêm các thao tác khác
    df = pd.read_csv('/opt/airflow/data/tiki_data_cleaned.csv')  

    print("Load thanh cong")

    # Kết nối tới PostgreSQL bằng psycopg2
    conn = psycopg2.connect(
        database="airflow",
        user="airflow",
        password="airflow",
        host="postgres",
        port="5432"
    )

    conn.autocommit = True
    cursor = conn.cursor()

    create_table_query = '''
    CREATE TABLE IF NOT EXISTS tiki_data (
        product_link TEXT,
        name TEXT,
        detail_cate TEXT,
        large_cate TEXT,
        image TEXT,
        price NUMERIC,
        discount NUMERIC,
        sale_quantity NUMERIC,
        rating_star NUMERIC,
        rating_quantity NUMERIC,
        "Công ty phát hành" TEXT,
        "Ngày xuất bản" TEXT,
        "Loại bìa" TEXT,
        "Số trang" NUMERIC,
        "Nhà xuất bản" TEXT,
        Bookcare TEXT,
        "Kích thước" TEXT,
        "Dịch Giả" TEXT,
        "Phiên bản sách" TEXT,
        describe TEXT,
        seller TEXT,
        seller_star NUMERIC,
        seller_reviews_quantity NUMERIC
    );
    '''

    cursor.execute(create_table_query)


    copy_csv = '''
               COPY tiki_data (product_link,name,detail_cate,large_cate,image,price,discount,sale_quantity,rating_star,
               rating_quantity,"Công ty phát hành","Ngày xuất bản","Loại bìa","Số trang","Nhà xuất bản",Bookcare,"Kích thước","Dịch Giả",
               "Phiên bản sách",describe,seller,seller_star,seller_reviews_quantity)
               FROM '/opt/airflow/data/tiki_data_cleaned.csv'
               DELIMITER ','
               CSV HEADER;
               '''
    cursor.execute(copy_csv)
    conn.close()
