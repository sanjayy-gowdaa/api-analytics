import numpy as np
import pandas as pd 
from faker import Faker
from datetime import datetime,timedelta
import random

fake=Faker()
np.random.seed(42)
NUM_ROWS=75000
START_DATE=datetime.now() -timedelta(days=30)

api_names = ["OCR_PAN", "OCR_AADHAAR", "FACE_MATCH", "KYC_VERIFY"]
document_types = ["PAN", "AADHAAR", "PASSPORT", "DRIVING_LICENSE"]
regions = ["Metro", "Tier-1", "Tier-2", "Rural"]
device_types = ["Android", "iOS", "Web"]

error_reasons = [
    "LOW_IMAGE_QUALITY",
    "BLURRY_IMAGE",
    "FACE_MISMATCH",
    "DOCUMENT_EXPIRED",
    "NETWORK_ERROR",
    "TIMEOUT",
    None  # success case
]

def generate_latency(api,success):
    base_latency = {
        "OCR_PAN": 1200,
        "OCR_AADHAAR": 1400,
        "FACE_MATCH": 900,
        "KYC_VERIFY": 700
    }[api]

    jitter = np.random.normal(0, 300)
    latency = base_latency + jitter

    if not success:
        latency += random.randint(300, 800)
    return max(200, int(latency))

def generate_status_and_error():
        success = np.random.rand() > 0.18
        if success:
            return 200, None
        else:
            status = random.choice([400, 401, 422, 500])
            error = random.choice(error_reasons[:-1])
            return status, error

logs=[]
for i in range(NUM_ROWS):
    api = random.choice(api_names)
    status_code, error_reason = generate_status_and_error()
    success = status_code == 200
    log = {
        "request_id": fake.uuid4(),
        "api_name": api,
        "timestamp": START_DATE + timedelta(
            minutes=random.randint(0, 60 * 24 * 30)
        ),
        "latency_ms": generate_latency(api, success),
        "status_code": status_code,
        "document_type": random.choice(document_types),
        "region": random.choices(
            regions, weights=[0.4, 0.3, 0.2, 0.1]
        )[0],
        "device_type": random.choices(
            device_types, weights=[0.6, 0.25, 0.15]
        )[0],
        "error_reason": error_reason
    }

    logs.append(log)

df = pd.DataFrame(logs)
df.sort_values("timestamp", inplace=True)
df.to_csv("raw_logs.csv", index=False)
print(f"generated {len(df)} API")