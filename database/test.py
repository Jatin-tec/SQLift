import psycopg2
import os
from psycopg2 import Error

# Load environment variables from .env.db file
from dotenv import load_dotenv

load_dotenv(".env.db")

print("Fetching database connection parameters from environment variables...")

# Database connection parameters
db_params = {
    "host": "172.18.0.2",  # assuming your PostgreSQL container is running on localhost
    "port": "5432",       # default PostgreSQL port
    "database": os.getenv("POSTGRES_DB"),  # replace with your actual database name
    "user": os.getenv("POSTGRES_USER"),           # replace with your actual username
    "password": os.getenv("POSTGRES_PASSWORD")         # replace with your actual password
}

table_name = "Transactions"  # replace with your actual table name

try:
    # Connect to the PostgreSQL server
    connection = psycopg2.connect(**db_params)

    # Create a cursor object using the cursor() method
    cursor = connection.cursor()

    # Execute a PostgreSQL query
    cursor.execute(f"""SELECT DISTINCT seller_desc FROM {table_name}""")  # replace with your actual table name

    # Fetch all the rows using the fetchall() method
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)

except Error as e:
    print("Error while connecting to PostgreSQL:", e)

finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")