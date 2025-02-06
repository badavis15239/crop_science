create schema data_a;
create schema data_b;
    create schema data_c;

CREATE TABLE data.weather_records (
    station_id VARCHAR(255),
    record_date DATE,
    max_temp DECIMAL,
    min_temp DECIMAL,
    precipitation DECIMAL,
    PRIMARY KEY (station_id, record_date) -- to avoid duplicates
);

CREATE INDEX idx_weather_records_date
ON data.weather_records  (record_date);


SET search_path TO your_schema_name;

show search_path;

CREATE TABLE IF NOT EXISTS data_c.weather_statistics (
    station_id TEXT NOT NULL,
    year INT NOT NULL,
    avg_max_temp_celsius NUMERIC(5,2),
    avg_min_temp_celsius NUMERIC(5,2),
    total_precipitation_cm NUMERIC(7,2),
    PRIMARY KEY (station_id, year)
);
