from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os


def main():
    spark = SparkSession.builder.appName("WebTrafficETL").getOrCreate()

    raw_data_path = "s3a://web-traffic-bucket-52fqs7r/raw/web_traffic_data.csv"

    df = spark.read.option("header", "true").csv(raw_data_path)

    print("Raw data schema:")
    df.printSchema()

    cleaned_df = df.filter(col("country").isNotNull())

    output_path = "s3a://web-traffic-bucket-52fqs7r/processed/web_traffic_data.parquet"
    cleaned_df.write.mode("overwrite").parquet(output_path)

    print(f"Processed data written to {output_path}")

    spark.stop()


if __name__ == "__main__":
    main()
