from .login_views import login_bp,login_manager
from .views import bp
import flask_login
def init_app(app):
    app.register_blueprint(bp)
    app.register_blueprint(login_bp)
    login_manager.init_app(app)
