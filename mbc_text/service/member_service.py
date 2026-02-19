from repository.member_repo import MemberRepo

class MemberService:

    @staticmethod
    def join(form: dict, profile_img_filename: str|None):
        uid = (form.get("uid")or "").strip()
        password = (form.get("password")or "").strip()
        name = (form.get("name")or "").strip()
        phone = (form.get("phone")or "").strip()
        email = (form.get("email")or "").strip()
        address = ((form.get("address")) or "").strip()

        if not all ([uid, password, name, phone, email, address]):
            return (False, "필수 항목을 입력하세요.")

        if MemberRepo.find_by_uid(uid):
            return (False,"이미 사용중인 아이디 입니다.")

        member = {
            "uid": uid,
            "password": password,
            "name": name,
            "phone": phone,
            "email": email,
            "address": address

        }
        ok = MemberRepo.insert(member)
        return (ok, "가입 완료" if ok else "가입 실패")

    @staticmethod
    def login(uid: str, password: str):
        if not uid or not password:
            return False, None, "아이디/비밀번호를 입력하세요."

        member = MemberRepo.find_by_uid(uid)
        if not member:
            return False, None, "존재하지 않는 아이디입니다."

        if member["password"] != password:
            return False, None, "비밀번호가 일치하지 않습니다."

        if not member["active"]:
            return False, None, "비활성화된 계정입니다."

        return True, member, None



