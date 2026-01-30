-- Active: 1760818633671@@127.0.0.1@3306@apidb

--avg latency
select api_name,ROUND(avg(latency_ms),2) as avg_latency_ms
from api_logs
GROUP BY api_name
ORDER BY avg_latency_ms DESC

--p95 latency
select api_name,
ANY_VALUE(latency_ms) as p95_latency
from (
    SELECT api_name,
    latency_ms,
    ntile(20) over(PARTITION BY api_name ORDER BY latency_ms) as tile
    from api_logs
) t 
WHERE tile=19
GROUP BY api_name

--success rate per api
SELECT api_name,
ROUND(SUM(CASE 
    WHEN status_Code=200 THEN 1  
    ELSE  0
END)*100/count(*),2) as success_rate_per_api
from api_logs
GROUP BY api_name
ORDER BY success_rate_per_api

--failure reason
select error_reason,
count(*) as error_count
from api_logs
where status_Code !=200
GROUP BY error_reason
ORDER BY error_count DESC

--region wise success rate
select region,
ROUND(sum(CASE 
    WHEN status_code=200 THEN 1  
    ELSE  0
END)*100/count(*),2) as success_rate_per_region
from api_logs
GROUP BY region
ORDER BY success_rate_per_region DESC

--conversion rate
SELECT api_name,
count(*) as total_requests,
ROUND(SUM(CASE 
    WHEN status_code=200 THEN 1 
    ELSE  0
END)*100/COUNT(*),2) as conversion_rate
from api_logs
GROUP BY api_name
ORDER BY conversion_rate DESC



SELECT *
FROM api_logs;

