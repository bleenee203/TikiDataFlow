# Tiki DATA PIPELINE USING APACHE AIRFLOW

This project involves building an automated pipeline to scrape, process, store, query, and visualize data. The goal is to create an end-to-end solution for collecting web data, processing it for further analysis, storing it in a structured format, and providing an interactive dashboard for data visualization and insights.

## Key Components:
1. Data Scraping with Airflow:

Apache Airflow is used to automate web scraping tasks from Tiki website, scheduling and orchestrating the data collection process through DAGs (Directed Acyclic Graphs).
Airflow ensures the scraped data is updated and available for processing on a regular schedule.
2. Data Processing

PySpark is used to efficiently process and transform large datasets.
Scraped data is cleaned, normalized, and structured which ensures scalable processing in distributed environments.
3. Data Storage and Querying in PostgreSQL:

Processed data is stored in PostgreSQL for reliable and structured storage.
PySpark queries the data stored in PostgreSQL, leveraging its powerful querying capabilities to perform efficient extraction and aggregation for analysis.
4. Data Visualization with Streamlit:

Developed interactive dashboards and visualizations using Streamlit.
The dashboards provide real-time insights and allow users to query, explore, and visualize data trends dynamically.
## Technologies Used:
Apache Airflow: For automating and scheduling the web scraping tasks.
PostgreSQL: For data storage and relational querying.
PySpark: For distributed data processing and querying.
Streamlit: For building interactive data visualizations.
## Outcome:
The pipeline enables automated, efficient data collection, processing, and querying at scale, while the Streamlit dashboard interactive visualizations to explore key insights. This end-to-end solution supports faster decision-making and provides actionable intelligence from the processed data.
