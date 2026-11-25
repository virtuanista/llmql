import os
from pathlib import Path

import MySQLdb
from dotenv import load_dotenv

from logger import db_errors

load_dotenv(Path(__file__).with_name('.env'))


def execute_query(query: str):
    try:
        connection = MySQLdb.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            passwd=os.getenv('DB_PASSWORD'),
            db=os.getenv('DB_NAME'),
            auth_plugin='mysql_native_password'
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            connection.close()
    except MySQLdb.MySQLError as e:
        # Solo el error: las credenciales nunca se registran.
        db_errors.error(f'Error executing query: {e}')
        raise
