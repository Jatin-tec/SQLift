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

# Specify the table for which you want to retrieve column names
table_name = "transactions"

def fetch_columns():
    response = None
    try:
        # Connect to the PostgreSQL server
        connection = psycopg2.connect(**db_params)

        # Create a cursor object using the cursor() method
        cursor = connection.cursor()

        # Execute a PostgreSQL query to get all column names of the specified table
        cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';")

        # Fetch all the column names using the fetchall() method
        columns = cursor.fetchall()

        response = []
        if columns:
            # Print the column names
            for column in columns:
                response.append(column[0])
            print(response)
        else:
            print(f"No such table '{table_name}' in the database.")

    except Error as e:
        print("Error while connecting to PostgreSQL:", e)
        return response
       
    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            return response

if __name__ == "__main__":
    fetch_columns()