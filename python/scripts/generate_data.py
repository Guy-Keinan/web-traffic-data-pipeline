import pandas as pd
import random
from datetime import datetime, timedelta


def generate_web_traffic_data(num_records):
    data = []

    for _ in range(num_records):
        session_id = f"sess_{random.randint(1000, 9999)}"
        user_id = f"user_{random.randint(100, 999)}"
        timestamp = datetime.now() - timedelta(minutes=random.randint(0, 10000))
        page = random.choice(["/home", "/about", "/contact", "/products", "/pricing"])
        referrer = random.choice(
            ["google.com", "facebook.com", "twitter.com", "linkedin.com", "direct"]
        )
        country = random.choice(["US", "UK", "DE", "FR", "IN", "JP"])
        browser = random.choice(["Chrome", "Firefox", "Safari", "Edge", "Opera"])

        data.append(
            {
                "session_id": session_id,
                "user_id": user_id,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "page": page,
                "referrer": referrer,
                "country": country,
                "browser": browser,
            }
        )

    df = pd.DataFrame(data)
    return df


def main():
    df = generate_web_traffic_data(100)
    output_path = "/opt/airflow/python/scripts/web_traffic_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Web traffic data generated and saved to {output_path}")


if __name__ == "__main__":
    main()
