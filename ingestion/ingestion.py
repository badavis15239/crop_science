import os
import psycopg2
import logging
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_db():
    # PostgreSQL Connection
    DB_CONFIG = {
        "dbname": os.getenv('DATABASE'),
        "user": os.getenv('ADMIN_USER'),
        "password": os.getenv('ADMIN_PASSWORD'),
        "host": os.getenv('HOST'),
        "port": os.getenv('PORT')
    }

    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    return conn, cursor


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

logging.info("Create constraints to ensure no dupes and create indexes")

cursor.execute("ALTER TABLE weather_records DROP CONSTRAINT IF EXISTS weather_records_pkey CASCADE; \
    ALTER TABLE weather_records ADD CONSTRAINT weather_records_pkey PRIMARY KEY (station_id, record_date);")

conn.commit()

logging.info("Constraints and indexes complete")

"""
If you want, you can create indexes but they aren't needed since we aren't querying specific 
attributes in the table such as date or temps etc.  Indexes and constraints are created after
data is loaded to allow for speed of loading.  If any failures occur in the constraints/index 
creation, then the schema never switches and the api user keeps using the old schema until the data
ingestion issues are resolved.
"""

"""
You could add a deduplicaton step here to ensure that there aren't any duplicate records.  However,
the data will fail to load because the there is a primary key constraint on station_id, and record_date
"""

## Swap live schema for api user so seemlessly changes the data source and no down time for api on data loads
if current_search_path[0] == 'data_a':
    cursor.execute(f"ALTER ROLE api_user SET search_path TO data_b, data_c;")
elif current_search_path[0] == 'data_b':
    cursor.execute(f"ALTER ROLE api_user SET search_path TO data_a, data_c;")
else:
    logging.error(f'Search path = {current_search_path}')

conn.commit()
