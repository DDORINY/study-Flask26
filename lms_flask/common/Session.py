import pymysql
from flask import session

class Session:

    @staticmethod
    def get_connection():
        return pymysql.connect(
            host='localhost',
            user='mbc',
            password='1234',
            db='lms',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    @staticmethod
    def is_login():
        return "user_id" in session

    @staticmethod
    def is_admin():
        return session.get('role') == "admin"

