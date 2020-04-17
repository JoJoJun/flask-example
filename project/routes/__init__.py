from .views import bp,login_manager
import flask_login
def init_app(app):
    app.register_blueprint(bp)
    login_manager.init_app(app)
