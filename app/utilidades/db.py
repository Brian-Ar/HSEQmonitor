from pymysql import connect
from pymysql.cursors import DictCursor
from dotenv import load_dotenv
import os

load_dotenv()

def obten_conexion():
    try:
        conn = connect(
            host=os.environ.get('HOST'),
            user=os.environ.get('USER'),
            password=os.environ.get('PASSWORD'),
            database=os.environ.get('DATABASE'),
            cursorclass=DictCursor
        )
        return conn
    except:
        return None