import json
import boto3
import requests
import os
from datetime import datetime

# Initialize AWS clients outside the handler for better performance
s3 = boto3.client('s3')
ssm = boto3.client('ssm')


def lambda_handler(event, context):
    try:
        # Retrieve API Key from SSM Parameter Store (SecureString)
        parameter = ssm.get_parameter(Name='/toledo/weather_api_key', WithDecryption=True)
        api_key = parameter['Parameter']['Value']

        # Fetch Toledo weather data of Toledo in Fahrenheit
        query = "Toledo,OH,US"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={query}&appid={api_key}&units=imperial"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Create folder structure for data partitioning (YYYY/MM/DD)
        # Faster queries when data is partitioned in the future
        now = datetime.now()
        year, month, day, hour = now.strftime('%Y'), now.strftime('%m'), now.strftime('%d'), now.strftime('%H')

        file_path = f"raw_data/year={year}/month={month}/day={day}/weather_{hour}.json"

        # Upload JSON data to S3 bucket
        bucket_name = "toledo-weather-energy-raw-st"

        s3.put_object(
            Bucket=bucket_name,
            Key=file_path,
            Body=json.dumps(data),
            ContentType='application/json'
        )

        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully saved data to {file_path}")
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {str(e)}")
        }