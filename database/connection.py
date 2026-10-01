import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "John",
    "database": "medical_inventory",
    "port": 3306
}


def get_connection():
    """
    Create and return a connection to the medical_inventory database.
    """

    try:
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            return connection

    except Error as error:
        print(f"MySQL connection error: {error}")

    return None