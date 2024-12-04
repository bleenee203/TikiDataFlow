# TIKI DATA PIPELINE USING APACHE AIRFLOW

This project involves building an automated pipeline to scrape, process, store, query, and visualize data. The goal is to create an end-to-end solution for collecting web data, processing it for further analysis, storing it in a structured format, and providing an interactive dashboard for data visualization and insights.

## Key Components:
**Data Pipeline with Airflow**:
Apache Airflow is used to automate extract (web scraping) tasks from Tiki website, scheduling and orchestrating the data collection process through DAGs (Directed Acyclic Graphs).
Airflow ensures the scraped data is updated and available for processing on a regular schedule. The pipeline includes the subsequent tasks: data transformation, loading, processing, and visualization, ensuring a scalable flow of information for analysis.

![image](https://github.com/user-attachments/assets/c5e80ee3-776b-4ead-86fa-fc61fce7cb9c)

**Extract**

Dataset crawled from Tiki

![image](https://github.com/user-attachments/assets/6a55db2f-3cc7-491d-9730-a117312c584e)

**Transform**

Python is used to efficiently process and transform datasets. Scraped data is cleaned, normalized, and structured which ensures scalable processing in distributed environments.

**Load**

Data Storage and Querying in PostgreSQL:
Processed data is stored in PostgreSQL for reliable and structured storage.

![image](https://github.com/user-attachments/assets/4f2a9909-19fa-46e1-82ae-9bf1be9bf6e8)

PySpark queries the data stored in PostgreSQL, leveraging its powerful querying capabilities to perform efficient extraction and aggregation for analysis.

- Query average rating points by supplier

![image](https://github.com/user-attachments/assets/004ebb9f-41e6-412a-b68a-5aa3ad01cc02)

- Calculate the correlation coefficient between price and sales quantity

![image](https://github.com/user-attachments/assets/11911b10-5f13-48ca-a69b-0dcaaf70ace3)

- Perform a query to retrieve products with a price above 100,000 and then store the query results into PostgreSQL with the new table name Tiki_data_filtered

![image](https://github.com/user-attachments/assets/ecda7cc9-057b-44f0-bebc-84b100ff5100)

**Data Visualization with Streamlit**: Developed interactive dashboards and visualizations using Streamlit.
The dashboards provide real-time insights and allow users to query, explore, and visualize data trends dynamically.

![image](https://github.com/user-attachments/assets/de389693-9a78-4216-9f3f-dea85a5b58ac)

![image](https://github.com/user-attachments/assets/eec0bce4-3399-4f09-9b8f-aaa9627d9288)

## Technologies Used:
Apache Airflow: For automating and scheduling the web scraping tasks.

PostgreSQL: For data storage and relational querying.

PySpark: For distributed data processing and querying.

Streamlit: For building interactive data visualizations.
## Outcome:
The pipeline enables automated, efficient data collection, processing, and querying at scale, while the Streamlit dashboard interactive visualizations to explore key insights. This end-to-end solution supports faster decision-making and provides actionable intelligence from the processed data.
