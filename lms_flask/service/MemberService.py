from common.Session import Session
from domain.Member import Member

class MemberService:

    # 로그인 검증
    @staticmethod
    def login(uid:str, pw:str):
        uid = (uid or "").strip()
        pw = (pw or "").strip()

        if not uid or not pw:
            raise ValueError("아이디와 비밀번호를 입력해주세요.")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT * 
                FROM members 
                WHERE uid = %s 
                LIMIT 1"""
                cursor.execute(sql, (uid,))
                row = cursor.fetchone()

                if not row:
                    raise ValueError("아이디가 존재하지 않습니다.")

                if int(row.get('active')) != 1:
                    raise ValueError("비활성화 계정입니다.")

                if row.get('password') != pw:
                    raise ValueError("비밀번호가 맞지 않습니다.")

                return Member.from_db(row)
        finally:
            conn.close()

    # 회원가입
    @staticmethod
    def join(uid:str, pw:str,name:str):
        uid = (uid or "").strip()
        pw = (pw or "").strip()
        name = (name or "").strip()

        if not uid or not pw or not name:
            raise ValueError("모두 입력해주세요.")

        conn = Session.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                SELECT id
                FROM members 
                WHERE uid = %s""",(uid,))
                row = cursor.fetchone()
                if row:
                    raise ValueError("중복된 아이디입니다.")

                sql = """
                INSERT INTO members (uid, password, name, role, active)
                VALUES (%s, %s, %s, 'user', 1)"""
                cursor.execute(sql,(uid,pw,name))
                conn.commit()
                member_id = cursor.lastrowid

                return Member(
                    id=member_id,
                    uid=uid,
                    pw=pw,
                    name=name,
                    role="user",
                    active=True
                )
        finally:
            conn.close()


