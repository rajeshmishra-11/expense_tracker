import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # my MySQL username
        password="rajeshji11",  # my MySQL password
        database="expense_tracker"
    )



