import os, uuid
from werkzeug.utils import secure_filename
from flask import current_app

# 허용할 이미지 촥장자 목록
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

def save_profile_image(file_storage:str):

    # 파일이 없거나 파일명이 비어 있는 겨우 -> 업로드 안 한 것으로 처리
    if not file_storage or file_storage.filename == "":
        return None

    #업로드된 원본 파일명을 안전한 이름으로 변환
    # 경로 조작 공격 방지
    filename = secure_filename(file_storage.filename)

    # 확장자 추출 (파일 명에 "."이 있는 경우만 처리
    ext = filename.split('.',1)[-1].lower() if '.' in filename else ""

    # 허용된 확장자가 아니면 예외발생
    if ext not in ALLOWED_EXT:
        raise ValueError ("invalid image ty")

    #uuid를 이용한 고유한 파일명 생성
    # 기존 파일 덮어쓰기 방지
    new_name = f"{uuid.uuid4().hex}.{ext}"

    # Flask 설정(config.py)에 정의된 업로드 디렉토리 경로 가져오기
    save_dir = current_app.config["UPLOAD_PROFILE_DIR"]

    #업로드 폴더가 없으면 자동 생성
    os.makedirs(save_dir, exist_ok=True)

    #실제 파일 저장
    file_storage.save(os.path.join(save_dir, new_name))

    # 저장된 파일명 변환(DB에 저장할 값
    return new_name