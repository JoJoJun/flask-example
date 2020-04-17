from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def init_app(app):
    db.init_app(app)
#
# # project/routes/__init__.py
# # from .users import user_bp
# # from .posts import posts_bp
# # ...
#
# # def init_app(app):
# #     app.register_blueprint(user_bp)
# #     app.register_blueprint(posts_bp)