import MySQLdb
import os
from dotenv import load_dotenv
import logging

# Load the .env file
load_dotenv(dotenv_path='d:/GitHub/llmql/.env')

# Debug logging to verify environment variables
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"DB_HOST: {os.getenv('DB_HOST')}")
logging.debug(f"DB_USER: {os.getenv('DB_USER')}")
logging.debug(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
logging.debug(f"DB_NAME: {os.getenv('DB_NAME')}")

connection = MySQLdb.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    passwd=os.getenv('DB_PASSWORD'),
    db=os.getenv('DB_NAME'),
    auth_plugin='mysql_native_password'
)

logging.basicConfig(filename='logs/db_errors.log', level=logging.ERROR)

def execute_query(query: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()
    except MySQLdb.MySQLError as e:
        logging.error(f'Error executing query: {e}')
        raise