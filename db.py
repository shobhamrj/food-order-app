import mysql.connector
from config import settings


mysql_conn = mysql.connector.connect(
    host=settings.db_host,
    user=settings.db_user,
    password=settings.db_pass,
    database=settings.db_database,
    port=settings.db_port
)
cursor = mysql_conn.cursor()

