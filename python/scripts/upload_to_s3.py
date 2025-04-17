import boto3

def main():
    bucket_name = "web-traffic-bucket-52fqs7r"
    file_path = "/opt/airflow/python/scripts/web_traffic_data.csv"
    object_name = "raw/web_traffic_data.csv"

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to s3://{bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

if __name__ == "__main__":
    main()
