CREATE TABLE IF NOT EXISTS regions_clean (
    region_id INT PRIMARY KEY,
    region VARCHAR(100) NOT NULL,
    population BIGINT NOT NULL,
    area_sq_km DECIMAL(15,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS disaster_events_clean (
    event_id INT PRIMARY KEY,
    disaster_type VARCHAR(50) NOT NULL,
    region VARCHAR(100) NOT NULL,
    event_date DATE NULL,
    severity VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS impact_assessment_clean (
    impact_id INT PRIMARY KEY,
    event_id INT NOT NULL,
    affected_people BIGINT NOT NULL DEFAULT 0,
    economic_loss_musd DECIMAL(15,2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_impact_event
        FOREIGN KEY (event_id) REFERENCES disaster_events_clean(event_id)
);
