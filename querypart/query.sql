CREATE DATABASE apidb

SHOW DATABASES

use apidb

create Table api_logs(
    request_id CHAR(36) PRIMARY KEY,
    api_name VARCHAR(50),
    TIMESTAMP DATETIME,
    latency_ms int,
    status_Code int,
    document_type VARCHAR(50),
    region VARCHAR(20),
    device_type VARCHAR(20),
    error_reason VARCHAR(50)
);

SELECT * FROM api_logs;
