class Member:

    def __init__(self,id,uid,pw,name,role="user",active=True):
        self.id = id
        self.uid = uid
        self.pw = pw
        self.name = name
        self.role = role
        self.active = active


    @classmethod
    def from_db(cls,row:dict):
        if not row:
            return None

        return cls(
            id = row.get('id'),
            uid = row.get('uid'),
            pw = row.get('password'),
            name = row.get('name'),
            role = row.get('role'),
            active = bool(row.get('active'))
        )