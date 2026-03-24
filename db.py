import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="dard-e-tanhai",
        database="complaint_routing_system"
    )