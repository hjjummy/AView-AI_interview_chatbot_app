from flask import Flask

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db=SQLAlchemy()
migrate=Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    # DB 설정
    db.init_app(app)
    migrate.init_app(app, db)

    # 블루프린트 등록
    from .views import main_views
    app.register_blueprint(main_views.bp)

    from . import models # 플라스크의 Migrate 기능이 인식될 수 있도록


    return app