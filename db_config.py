import pymysql

def get_db_connection():
    return pymysql.connect(
        host="dpg-cuacr73qf0us73c869g0-a",
        user="root",
        password="u3Q6m50wS9TcrxI4N8GjGIlTccHH83jI",
        database="expense_tracker_g6lz",
        port=5432,
        charset="utf8mb4",
    )
