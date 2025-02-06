import os
import psycopg2
import logging
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_db():
    # PostgreSQL Connection
    DB_CONFIG = {
        "dbname": "data",
        "user": "admin",
        "password": "admin",
        "host": "localhost",
        "port": "5432"
    }

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    return conn, cursor

# def create_query(query):
#     # Create Staging Table (Temporary for Fast Bulk Load)
#     staging_table_query = """
    
#     """
#     return staging_table_query

# Function to Process and Load Each File
def process_file(file_path, conn, cursor):
    station_id = os.path.basename(file_path).split('.')[0]  # Extract station ID from filename
    temp_file_path = file_path + ".cleaned"

    # Convert the file into a cleaned version for COPY
    with open(file_path, "r") as infile, open(temp_file_path, "w") as outfile:
        infile.readline()  # Skip header if present
        for line in infile:
            columns = line.strip().split("\t")
            if len(columns) < 4:  # Skip malformed lines
                continue

            try:
                record_date = datetime.strptime(columns[0], "%Y%m%d").strftime("%Y-%m-%d")
                max_temp = "\\N" if columns[1] == "-9999" else columns[1]  # Convert -9999 to NULL
                min_temp = "\\N" if columns[2] == "-9999" else columns[2]
                precipitation = "\\N" if columns[3] == "-9999" else columns[3]

                outfile.write(f"{station_id}\t{record_date}\t{max_temp}\t{min_temp}\t{precipitation}\n")

            except Exception as e:
                logging.error(f"Error processing line: {line}. Error: {e}")
                continue

    # Bulk Insert with COPY
    try:
        with open(temp_file_path, "r") as f:
            cursor.copy_expert(
                "COPY weather_records FROM STDIN WITH (FORMAT CSV, DELIMITER E'\t', NULL '\\N')", f
            )
        conn.commit()
        logging.info(f"Loaded file: {file_path}")
    except Exception as e:
        conn.rollback()
        logging.error(f"COPY failed for {file_path}. Error: {e}")

    os.remove(temp_file_path)  # Clean up temp file


conn, cursor = connect_db()
# Set the search path to data_a schema
cursor.execute("SHOW search_path;")

# Fetch the result
current_search_path = cursor.fetchone()
import pdb; pdb.set_trace()
if current_search_path[0] == 'data_a':
    cursor.execute("ALTER ROLE admin SET search_path TO data_b;")
elif current_search_path[0] == 'data_b':
    cursor.execute("ALTER ROLE admin SET search_path TO data_a;")
else:
    logging.error(f'Search path = {current_search_path}')
conn.commit()
cursor.execute("DROP TABLE IF EXISTS weather_records; \
    CREATE TABLE weather_records ( \
        station_id TEXT, \
        record_date DATE, \
        max_temp REAL, \
        min_temp REAL, \
        precipitation REAL \
    );")

conn.commit()
logging.info(f"Table created")

# Process All Files in the Directory
folder_path = "../../code-challenge-template/wx_data/"
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    process_file(file_path, conn, cursor)

logging.info("Data loaded")

##### last steps -- dedup and swap schema to read from schema where the data was loaded

# # Deduplicate and Move Data to Final Table
# deduplication_query = """
# INSERT INTO weather_records (station_id, record_date, max_temp, min_temp, precipitation)
# SELECT DISTINCT station_id, record_date, max_temp, min_temp, precipitation
# FROM weather_records
# ON CONFLICT (station_id, record_date) DO NOTHING;
# """
# cursor.execute(deduplication_query)
# conn.commit()
# logging.info("✅ Deduplication completed.")

# # Close Connection
# cursor.close()
# conn.close()
# logging.info("✅ All operations completed successfully!")
