import logging
import mysql.connector
from mysql.connector import Error
from ..config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

logger = logging.getLogger(__name__)

def create_mysql_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        if connection.is_connected():
            print("Connection to MySQL DB successful")
            logger.info("Successfully connected to MySQL")
    except Error as e:
        print(f"The error '{e}' occurred")
        logger.error(f"Error during MySQL connection: {e}")
    return connection

def execute_query(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully")
        logger.info("Successfully executed query")

    except Error as e:
        print(f"The error '{e}' occurred")
        logger.error(f"Error during query execution: {e}")

