from common.db import get_connection

class AdminService:
    @staticmethod
    def get_dashboard():
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) cnt FROM members")
                total = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) cnt FROM members WHERE active=1")
                active = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) cnt FROM members WHERE active=0")
                inactive = cursor.fetchone()["cnt"]
                cursor.execute("SELECT COUNT(*) cnt FROM members WHERE DATE(created_at)=CURDATE()")
                today_join = cursor.fetchone()["cnt"]
            return{
                "total": total,
                "active": active,
                "inactive": inactive,
                "today_join": today_join,
                "today_inquiry": 0,  # 문의 테이블 붙이면 교체
                }
        finally:
            conn.close()
