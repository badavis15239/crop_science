import os
import psycopg2

# Database connection details
DB_CONFIG = {
    "dbname": os.getenv('DATABASE'),
    "user": os.getenv('ADMIN_USER'),
    "password": os.getenv('ADMIN_PASSWORD'),
    "host": os.getenv('HOST'),
    "port": os.getenv('PORT')
}

def calculate_and_store_weather_statistics():
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Query to aggregate data
        query = """
            INSERT INTO data_c.weather_statistics (station_id, year, avg_max_temp_celsius, avg_min_temp_celsius, total_precipitation_cm)
            SELECT 
                station_id,
                EXTRACT(YEAR FROM record_date) AS year,
                ROUND(CAST(AVG(max_temp) / 10.0 AS NUMERIC), 2) AS avg_max_temp_celsius,
                ROUND(CAST(AVG(min_temp) / 10.0 AS NUMERIC), 2) AS avg_min_temp_celsius,
                ROUND(CAST(SUM(precipitation) / 100.0 AS NUMERIC), 2) AS total_precipitation_cm
            FROM weather_records
            GROUP BY station_id, year
            ON CONFLICT (station_id, year) DO UPDATE
            SET 
                avg_max_temp_celsius = EXCLUDED.avg_max_temp_celsius,
                avg_min_temp_celsius = EXCLUDED.avg_min_temp_celsius,
                total_precipitation_cm = EXCLUDED.total_precipitation_cm;
        """
        
        # Execute the query
        cursor.execute(query)
        conn.commit()
        print("Weather statistics calculated and stored successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Run the function
calculate_and_store_weather_statistics()
