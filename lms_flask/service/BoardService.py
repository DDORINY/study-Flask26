from domain import *
class BoardService:
    # C 게시글 생성
    @staticmethod
    def board_write(uid:str,member_id:int,title:str,content:str):
        uid = (uid or "").strip()
        member_id = (member_id or "").strip()
        title = (title or "").strip()
        content = (content or "").strip()

