# 🌐 Web Traffic ETL Pipeline

This project is a **ETL pipeline** built using **Apache Airflow**, **PySpark**, and **AWS S3**. It simulates web traffic data, processes it with Spark, and generates a report of the most visited pages.

The pipeline is containerized with Docker and orchestrated using Airflow to ensure modular, scalable, and production-ready data workflows.

---

## 🔧 Tech Stack

- **Airflow** – DAG orchestration & scheduling
- **Python** – Data generation & report creation
- **Spark (PySpark)** – Large-scale data processing
- **Docker** – Containerized development
- **AWS S3** – Cloud data storage (raw + processed)
- **Terraform** – Infrastructure provisioning (S3 bucket)

---

## 📊 What It Does

1. **Generate** synthetic web traffic data in CSV format.
2. **Upload** raw data to AWS S3.
3. **Run Spark job** to process the data (group, clean, transform).
4. **Save** processed data as Parquet into S3.
5. **Generate a report** with most visited pages from the Parquet file.
6. (Optional) **Upload the report back to S3**.

---

## 🚀 How to Run the Project

### 1. 🧱 Clone and Setup

```bash
git clone https://github.com/Guy-Keinan/web-traffic-data-pipeline.git
cd web-traffic-data-pipeline
pip install -r requirements.txt
```

### 2. 🛠️ Create `.env` File

Create a `.env` file in the root directory with your AWS credentials:

```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

> 🔐 These are needed to access S3 buckets from inside containers.

---

### 3. ☁️ Provision AWS S3 Bucket

Using Terraform (inside `/terraform` folder):

```bash
cd terraform
terraform init
terraform apply
```

This creates an S3 bucket:  
`web-traffic-bucket-<your-id>`

---

### 4. 🐳 Run Docker Containers

```bash
docker-compose up --build -d
```

This will:
- Start Airflow webserver, scheduler, Spark, Postgres
- Mount your local scripts to containers

---

### 5. 💻 Access Airflow

Open in browser:  
[http://localhost:8080](http://localhost:8080)

Login:
```
Username: airflow
Password: airflow
```

Trigger the DAG: `web_traffic_etl_pipeline`

---

## 📁 File Structure

```
├── airflow/
│   ├── dags/
│   │   └── etl_pipeline.py       # Airflow DAG definition
│   └── logs/
├── python/
│   └── scripts/
│       ├── generate_data.py      # Raw data generator
│       ├── read_processed_data.py# Local helper to view processed output
│       └── web_traffic_report.csv# Output report
├── spark/
│   └── src/
│       └── job.py                # PySpark transformation script
├── terraform/
│   └── main.tf                   # Terraform S3 bucket setup
├── docker-compose.yml
└── .env                          # AWS credentials
```

---

## 📌 Output Example

Final report (`web_traffic_report.csv`):

```
page,visit_count
/home,27
/contact,20
/products,19
/about,18
/pricing,16
```

---

## 👤 Author

Built by Guy Keinan
For educational use, backend/data engineering practice.