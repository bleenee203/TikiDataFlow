# import pandas as pd 
# import os
# # from pyspark.sql import SparkSession


# def process_tiki_data(**kwargs):
#     print("Process Tiki data...")

#     # Khởi tạo SparkSession
#     spark = SparkSession.builder \
#     .appName("LargeDataProcessing") \
#     .config("spark.executor.memory", "4g") \
#     .config("spark.executor.cores", "4") \
#     .config("spark.sql.shuffle.partitions", "200") \
#     .getOrCreate()


#     # Đọc dữ liệu từ CSV vào DataFrame Spark
#     df = spark.read.csv("/opt/airflow/data/tiki_data.csv", header=True, inferSchema=True)

#     # Hiển thị dữ liệu
#     df.show()

#     # Truy vấn dữ liệu lớn bằng Spark SQL
#     df.createOrReplaceTempView("tiki_data")
#     spark.sql("SELECT * FROM tiki_data WHERE price > 100000").show()
#     spark.stop()
from pyspark.sql import SparkSession

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
    .getOrCreate()

 # .config("spark.executor.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar") \
    # .config("spark.driver.extraClassPath", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar") \
sc = spark.sparkContext
print("Dang doc du lieu tu CSV:")
df = spark.read.csv("/opt/airflow/data/tiki_data_cleaned.csv", header=True, inferSchema=True)

    # Hiển thị dữ liệu
df.show()
print("Da doc du lieu tu CSV THANH CONG")

# print("Dang doc du lieu tu PostgreSQL")
# # Cấu hình thông tin PostgreSQL
# jdbc_url = "jdbc:postgresql://postgres:5432/airflow"

# # Đọc dữ liệu từ PostgreSQL
# df = spark.read \
#     .format("jdbc") \
#     .option("url", jdbc_url) \
#     .option("dbtable", "tiki_data") \
#     .option("user", "airflow")\
#     .option("password", "airflow")\
#     .load()

# # Hiển thị dữ liệu
# df.show()

print("Truy van du lieu ne")
# Truy vấn dữ liệu lớn bằng Spark SQL
df.createOrReplaceTempView("tiki_data")
result_df = spark.sql("SELECT * FROM tiki_data WHERE price > 100000")
# spark.sql("SELECT * FROM tiki_data WHERE price > 100000").show()

result_df.describe().show()  # Hiển thị các thống kê cơ bản

result_df.write.format("csv").mode("overwrite").save("./data/output_tiki_data.csv", header=True)
print("Xuat file CSV thanh cong!")

spark.stop()