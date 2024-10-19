from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, avg

print("Processing vui long doi")


spark = SparkSession.builder \
    .appName("TikiDataProcessing") \
    .config("spark.master", "spark://spark-master:7077") \
    .config("spark.executor.memory", "6g") \
    .config("spark.executor.cores", "6") \
    .config("spark.rpc.askTimeout", "600s")\
    .config("spark.network.timeout", "1200s") \
    .config("spark.executor.heartbeatInterval", "200s") \
    .config("spark.sql.shuffle.partitions", "200")\
    .config("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar") \
    .getOrCreate()


sc = spark.sparkContext

print("Dang doc du lieu tu PostgreSQL")
# Cấu hình thông tin PostgreSQL
jdbc_url = "jdbc:postgresql://postgres:5432/airflow"

# Đọc dữ liệu từ PostgreSQL
df = spark.read \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "tiki_data") \
    .option("user", "airflow")\
    .option("password", "airflow")\
    .option("driver", "org.postgresql.Driver") \
    .load()

# # # Hiển thị dữ liệu
df.show()

# Phân vùng dữ liệu
df = df.repartition(4)

# Lưu trữ DataFrame trong bộ nhớ đệm
df.cache()
df.count()
print("DataFrame đã được lưu trữ trong bộ nhớ đệm.")

# Thực hiện phân tích dữ liệu
# Kiểm tra kiểu dữ liệu
df.printSchema()

# 1. Tổng số lượng bán theo danh mục
# Kiểm tra xem có giá trị null hoặc không hợp lệ trong cột sale_quantity
df.filter(df["sale_quantity"].isNull()).show()

# Nếu có null,Thay thế các giá trị null bằng giá trị 0
df = df.fillna({"sale_quantity": 0})
# Chuyển đổi cột sale_quantity từ kiểu decimal sang float
df = df.withColumn("sale_quantity", col("sale_quantity").cast("float"))
sales_summary = df.groupBy("large_cate").agg(sum("sale_quantity").alias("total_sales"))
print("Tổng số lượng bán theo danh mục:")
sales_summary.show()

# 2. Điểm đánh giá trung bình theo nhà cung cấp
df.filter(df["seller_star"].isNull()).show()
# Nếu có null,Thay thế các giá trị null bằng giá trị 0
df = df.fillna({"seller_star": 0})
# Chuyển đổi cột sale_quantity từ kiểu decimal sang float
df = df.withColumn("seller_star", col("seller_star").cast("float"))
seller_rating = df.groupBy("seller").agg(avg("seller_star").alias("avg_seller_rating"))
print("Điểm đánh giá trung bình theo nhà cung cấp")
seller_rating.show()

# 3. Hệ số tương quan giữa giá và số lượng bán
df.filter(df["price"].isNull()).show()
# Nếu có null,Thay thế các giá trị null bằng giá trị 0
df = df.fillna({"price": 0})
# Chuyển đổi cột sale_quantity từ kiểu decimal sang float
df = df.withColumn("price", col("price").cast("float"))
correlation = df.stat.corr("price", "sale_quantity")
print(f"Hệ số tương quan giữa giá và số lượng bán: {correlation}")

# Giải phóng bộ nhớ đệm
df.unpersist()
print("Đã giải phóng bộ nhớ đệm.")

print("Truy van du lieu ne")
# Truy vấn dữ liệu lớn bằng Spark SQL
df.createOrReplaceTempView("tiki_data")
result_df = spark.sql("SELECT * FROM tiki_data WHERE price > 100000")

result_df.describe().show()  # Hiển thị các thống kê cơ bản

# Ghi dữ liệu vào PostgreSQL
print("Dang ghi du lieu vao PostgreSQL")
result_df.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "tiki_data_filtered") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .option("driver", "org.postgresql.Driver") \
    .mode("overwrite")\
    .save()

print("Da ghi du lieu vao PostgreSQL thanh cong")

spark.stop()