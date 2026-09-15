-- Part 1 users who had concurrent sessions
SELECT DISTINCT a.name
FROM enriched_session_logs a
JOIN enriched_session_logs b
  ON a.name = b.name
WHERE a.session_id != b.session_id
  AND a.start_time < b.end_time
  AND b.start_time < a.end_time
;
/*
Output of the above query
"Avery Chen"
"Carol Williams"
"Casey Nguyen"
"Jamie Martinez"
"Jordan Patel"
"Morgan Rivera"
"Riley Thompson"
"Taylor Brooks"
*/

-- Part 2 
WITH concurrent_counts AS (
    SELECT 
        a.name,
        a.session_id,
        a.start_time,
        COUNT(b.session_id) AS active_at_start
    FROM enriched_session_logs a
    JOIN enriched_session_logs b
      ON a.name = b.name
     AND b.start_time <= a.start_time
     AND b.end_time > a.start_time
    GROUP BY a.name, a.session_id, a.start_time
)
SELECT 
    name, 
    MAX(active_at_start) AS max_concurrent_sessions
FROM concurrent_counts
WHERE active_at_start > 1
GROUP BY name
ORDER BY max_concurrent_sessions DESC, name ASC;

/*
Output of the above query
"Jamie Martinez"	6
"Casey Nguyen"	    5
"Riley Thompson"	4
"Taylor Brooks"	    4
"Jordan Patel"	    3
"Morgan Rivera"	    3
"Avery Chen"	    2
"Carol Williams"	2
*/