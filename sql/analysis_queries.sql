-- Disaster Affected Region Tracker Analysis
-- Run after loading the clean tables.

-- 1. Top 5 regions by total affected population
SELECT
    e.region,
    SUM(i.affected_people) AS total_affected_people
FROM disaster_events_clean e
JOIN impact_assessment_clean i ON e.event_id = i.event_id
GROUP BY e.region
ORDER BY total_affected_people DESC
LIMIT 5;

-- 2. Disaster severity distribution by disaster type
SELECT
    disaster_type,
    severity,
    COUNT(*) AS disaster_count
FROM disaster_events_clean
GROUP BY disaster_type, severity
ORDER BY disaster_type, disaster_count DESC;

-- 3. Monthly disaster trend
SELECT
    DATE_FORMAT(event_date, '%Y-%m') AS month,
    COUNT(*) AS disaster_count
FROM disaster_events_clean
WHERE event_date IS NOT NULL
GROUP BY DATE_FORMAT(event_date, '%Y-%m')
ORDER BY month;

-- 4. Economic loss vs affected population
SELECT
    e.event_id,
    e.region,
    e.disaster_type,
    i.affected_people,
    i.economic_loss_musd
FROM disaster_events_clean e
JOIN impact_assessment_clean i ON e.event_id = i.event_id
ORDER BY i.affected_people DESC;

-- 5. Region-wise disaster frequency
SELECT
    region,
    disaster_type,
    COUNT(*) AS disaster_count
FROM disaster_events_clean
GROUP BY region, disaster_type
ORDER BY region, disaster_type;
