import pandas as pd
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

s3_path = "s3://web-traffic-bucket-52fqs7r/processed/web_traffic_data.parquet"

print("📦 Reading processed Parquet data from S3...")
df = pd.read_parquet(
    s3_path,
    engine="pyarrow",
    storage_options={
        "key": AWS_ACCESS_KEY_ID,
        "secret": AWS_SECRET_ACCESS_KEY,
    },
)

print("Data Sample:")
print(df.head())

print("\nData Schema:")
print(df.dtypes)

print(f"\nNumber of rows: {len(df)}")

print("\nSummary statistics:")
print(df.describe(include="all"))
