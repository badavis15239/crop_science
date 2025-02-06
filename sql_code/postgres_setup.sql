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



to do

1.  automate schema and user creation when dockercompose up happens
2.  sql connection os.getenv
3.  create user for api_user
4.  ingestion -- swap schemas for ingestion, ingest, swap schema for api
6.  aws instructions for deployment (include ecs, eks and this should be an apigateway/lambda)
7.  dockerfile for api -- add to docker compose

Things I want to improve but ran out of time

1. mock tests and more unittests 
2. use the escape module to prevent sql injections
3.  Restritctions on the size of pages
4.  add additional parameters so people can queyr by year, weather station or both
5.  May be better to make a view out of the stats data 