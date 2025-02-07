create schema data_a;
create schema data_b;
create schema data_c;

ALTER ROLE admin SET search_path TO data_a, data_c; 

CREATE USER api_user WITH PASSWORD 'api_user';
GRANT USAGE ON SCHEMA data_a, data_b, data_c TO api_user;
GRANT SELECT ON ALL TABLES IN SCHEMA data_a, data_b, data_c TO api_user;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA data_a, data_b, data_c TO api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA data_a, data_b, data_c
GRANT USAGE, SELECT ON SEQUENCES TO api_user;

GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA data_a, data_b, data_c TO api_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA data_a, data_b, data_c
GRANT SELECT ON TABLES TO api_user;


CREATE TABLE IF NOT EXISTS data_c.weather_statistics (
    station_id TEXT NOT NULL,
    year INT NOT NULL,
    avg_max_temp_celsius NUMERIC(5,2),
    avg_min_temp_celsius NUMERIC(5,2),
    total_precipitation_cm NUMERIC(7,2),
    PRIMARY KEY (station_id, year)
);