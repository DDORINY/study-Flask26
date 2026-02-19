from common.db import get_connection

class MemberRepo:
    #uid 찾기
    @staticmethod
    def find_by_uid(uid:str):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM members WHERE uid=%s"
                cursor.execute(sql,(uid,))
                return cursor.fetchone()
        finally:
            conn.close()

    #회원의 id찾기
    @staticmethod
    def find_by_id(member_id:int):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM members WHERE id=%s"
                cursor.execute(sql,(member_id,))
                return cursor.fetchone()
        finally:
            conn.close()


    #회원가입 시 추가
    @staticmethod
    def insert(member:dict):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO members
                (uid,password,name,phone,email,address,role, active, profile_img)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

                cursor.execute(sql,(
                    member["uid"],
                    member["password"],
                    member["name"],
                    member["phone"],
                    member["email"],
                    member["address"],
                    member.get("role", "USER"),
                    1,
                    member.get("profile_img")
                ))
                conn.commit()
                return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    # 회원정보수정
    @staticmethod
    def update(member_id:int,name:str,phone:str,email:str,address:str,profile_img:str | None):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:

                #프로필 이미지가 있는 경우
                if profile_img:
                    sql = """
                    UPDATE members 
                    SET name =%s, phone= %s, email = %s, address =%s, profile_img=%s 
                    WHERE id=%s"""
                    cursor.execute(sql,(name,phone,email,address,profile_img,member_id))

                # 프로필 이미지가 없는 경우
                else:
                    sql = """
                    UPDATE members 
                    SET name =%s, phone= %s, email = %s, address =%s
                    WHERE id = %s"""
                    cursor.execute(sql,(name,phone,email,address,member_id,))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    # 회원탈퇴 시 비활성화 처리된다.
    @staticmethod
    def delete(member_id:int):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE members 
                SET active = 0
                WHERE id = %s """
                cursor.execute(sql,(member_id,))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    # 관지자 목록에서 키워드로 검색
    @staticmethod
    def list_members(active=None,keyword=None):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT id, uid,name,phone,email,address,active, created_at
                 FROM members
                 WHERE 1=1"""
                params=[]
                if active in (0, 1, True, False):
                    sql += " AND active = %s"
                    params.append(int(active))
                if keyword :
                    sql += " AND (uid LIKE %s OR name LIKE %s OR email LIKE %s )"
                    like =f"%{keyword}%"
                    params.extend([like, like, like]) # 체크하기
                sql += " ORDER BY created_at DESC"
                cursor.execute(sql,params)
                return cursor.fetchall()
        finally:
            conn.close()

    #관지라 비활성화 (탈퇴처리)
    @staticmethod
    def admin_disable(member_id:int):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE members 
                SET active = 0
                WHERE id = %s """
                cursor.execute(sql,(member_id,))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def admin_enable(member_id:int):
        conn=get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                UPDATE members 
                SET active = 1
                WHERE id = %s """
                cursor.execute(sql,(member_id,))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()


