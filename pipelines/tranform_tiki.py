import pickle
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def transform_tiki_data():
    print("Transform...")
    
    df = pd.read_csv('/opt/airflow/data/tiki_data.csv')
    print("Dữ liệu đã được tải")
    # Delete collumn unnecessary
    columns_to_drop = [
        'Địa chỉ tổ chức chịu trách nhiệm về hàng hóa',
        'Tên đơn vị/tổ chức chịu trách nhiệm về hàng hóa',
        'Ngôn ngữ',
        'Phương thức giao hàng Seller Delivery',
        'Phiên bản'
    ]
    df.drop(columns=columns_to_drop, inplace=True)

    # Convert negative numbers to positive numbers
    df['discount'] = df['discount'].abs()

    # Convert "So Trang" to Int
    # Bước 1: Chuyển các giá trị chuỗi không phải số thành NaN
    df['Số trang'] = pd.to_numeric(df['Số trang'], errors='coerce')

    # Bước 2: Lấy giá trị "Số trang" từ các quyển sách có cùng "large_cate"
    for index, row in df.iterrows():
        if pd.isna(row['Số trang']):
            # Lấy giá trị "Số trang" của quyển sách có large_cate tương tự
            similar_large_cate_value = df[df['large_cate'] == row['large_cate']]['Số trang'].dropna().mode()
            similar_value = df['Số trang'].dropna().mode()
            if not similar_large_cate_value.empty:
                df.at[index, 'Số trang'] = similar_large_cate_value[0]
            else: 
                df.at[index, 'Số trang'] = similar_value[0]

    # Bước 3: Chuyển cột "Số trang" sang kiểu int
    df['Số trang'] = df['Số trang'].astype(int)

    # Export
    df.to_csv('./data/tiki_data_cleaned.csv', index=False)
