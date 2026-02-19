import os

class Config:
    SECRET_KEY = "mbc_text_secret"
    DB_HOST = "192.168.0.161"
    DB_USER = "text"
    DB_PASSWORD = "1234"
    DB_NAME = "mbc_text"

    UPLOAD_PROFILE_DIR = os.path.join("static", "uploads", "profile")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB