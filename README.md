# AWS Serverless Weather Data Pipeline (ETL)

## 📌 Project Overview
[cite_start]This project implements an end-to-end serverless ETL (Extract, Transform, Load) pipeline on AWS to automate the collection, storage, and analysis of real-time weather data for Toledo, Ohio[cite: 25, 26]. [cite_start]The system is designed to be cost-effective and scalable, handling real-world data engineering challenges such as **Schema Evolution** and **Data Localization**[cite: 29, 30].

## 🏗️ Architecture
The pipeline architecture leverages the following AWS services:
* [cite_start]**Data Ingestion**: An **AWS Lambda** function triggered by **Amazon EventBridge** every hour to fetch data from the OpenWeather API[cite: 7, 26].
* [cite_start]**Security**: API credentials and sensitive configurations are managed securely using **AWS SSM Parameter Store**[cite: 7, 28].
* [cite_start]**Data Lake**: Raw JSON data is stored in **Amazon S3** using **Hive-style partitioning** (`year/month/day`) to optimize query performance and reduce costs[cite: 7, 27].
* [cite_start]**Data Cataloging**: **AWS Glue Crawlers** automatically scan S3 buckets to manage the metadata catalog and handle **Schema Evolution**[cite: 7, 29].
* [cite_start]**Analytics**: **Amazon Athena** is used to perform SQL-based transformations, including unit conversions and timezone adjustments[cite: 7, 30].

[Image of AWS data pipeline architecture diagram showing Lambda to S3 to Glue to Athena flow]

## 🚀 Key Features
* [cite_start]**Automated Partitioning**: Implemented a folder structure in S3 that allows Athena to skip unnecessary data, significantly lowering data scan costs[cite: 27].
* [cite_start]**Schema Resilience**: Successfully managed data type consistency using the Glue Data Catalog to handle inconsistent API responses (e.g., Integer to Double conversion)[cite: 29].
* [cite_start]**Data Transformation**: Engineered a SQL View to provide human-readable metrics[cite: 30]:
    * Converted temperatures from **Fahrenheit to Celsius**.
    * Localized observation times from **UTC to Eastern Standard Time (EST)**.
    * Flattened complex nested JSON structures for efficient querying.

## 🛠️ Tech Stack
* [cite_start]**Cloud**: AWS (Lambda, S3, Glue, Athena, EventBridge, SSM)[cite: 7].
* [cite_start]**Languages**: Python (Boto3), SQL (Advanced)[cite: 9].
* [cite_start]**Data Format**: JSON[cite: 8].

## 📊 Sample Analytics Query
To retrieve and view the processed data, you can query the established Athena View:

```sql
SELECT 
    city, 
    temp_f, 
    temp_c, 
    toledo_time, 
    sky_condition 
FROM v_toledo_weather_report 
ORDER BY toledo_time DESC 
LIMIT 10;