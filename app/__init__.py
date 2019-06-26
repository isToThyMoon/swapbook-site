from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登陆或注册'
    mail.init_app(app)
    # db.init_app 方法没有保存核心对象 只作临时参数 所以create_all()方法还要传入核心对象
    # 或者 让create_all 自己寻找current_app 传入
    # with app.app_context():
    #   db.create_all()
    # 或者 一开始在model中实例化db = SQLAlchemy() 时 把app 作为属性 参数传入 但是不同模块导入app实例太过麻烦
    db.create_all(app=app)

    return app


def register_blueprint(app):
    from app.web import web
    app.register_blueprint(web)
