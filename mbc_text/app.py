import os

from Tools.scripts.texi2html import spprog
from flask import Flask
from config import Config

from routes.main_routes import bp as main_bp
from routes.member_routes import bp as member_bp
from routes.admin_routes import bp as admin_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 업로드 폴더 자동 생성
    os.makedirs(app.config["UPLOAD_PROFILE_DIR"], exist_ok=True)

    # Blueprint 등록
    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(admin_bp)



    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)