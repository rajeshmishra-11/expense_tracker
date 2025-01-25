import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("dpg-cuacr73qf0us73c869g0-a"),
        user=os.getenv("root"),
        password=os.getenv("u3Q6m50wS9TcrxI4N8GjGIlTccHH83jI"),
        database=os.getenv("expense_tracker_g6lz"),
        port=int(os.getenv("5432")),
        charset="utf8mb4",
    )




