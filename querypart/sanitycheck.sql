SELECT count(*) from api_logs

SELECT status_code,count(*)
from api_logs
GROUP BY status_Code
ORDER BY COUNT(*) DESC
