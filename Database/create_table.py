import psycopg2
import csv
import os


# Load environment variables from .env.db file
from dotenv import load_dotenv

load_dotenv("../.env.db")

print("Creating table and importing data from CSV file...")
print("This might take a while...")

# Database connection parameters
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = "172.18.0.2"  # Because the PostgreSQL container is running on the same host
port = "5432"  # Default PostgreSQL port


# CSV file path
csv_file_path = "../dataset.csv"

# Establish database connection
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

# Read the header of the CSV file to get column names and data types
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)  # Read the first row as header

# Create table SQL statement dynamically based on CSV header
create_table_query = "CREATE TABLE IF NOT EXISTS table_name ({});".format(", ".join("{} VARCHAR(5000)".format(column) for column in header))
table_name = "Transactions"
create_table_query = create_table_query.replace("table_name", table_name)

# Execute the create table query
cur.execute(create_table_query)
conn.commit()

# Import data from CSV file
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row
    for row in csvreader:
        # Prepare SQL statement to insert data into the table
        insert_query = "INSERT INTO {} ({}) VALUES ({});".format(
            table_name,
            ", ".join(header),
            ", ".join(["%s"] * len(header))
        )
        cur.execute(insert_query, row)

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()

print("Table created and data imported successfully.")