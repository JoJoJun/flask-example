import flask_login
from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint
## 登录的路由和逻辑都在这页了
bp = Blueprint('login', __name__, url_prefix='/account')
login_manager = flask_login.LoginManager()


# users = {'foo@bar.tld': {'password': 'secret'}}
@login_manager.user_loader
def load_user(account):
    return User.query.get(account)


# @login_manager.request_loader
# def request_loader(request):
#     account = request.form.get('account')
#     user = User.query.get(account)
#     if not user:
#         return None
#
#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['password'] == user.password
#     return user


@bp.route('/login', methods=['GET', 'POST'])
def login():
    print("in login!!!!!")
    if request.method == 'GET':
        return render_template('login.html',user=flask_login.current_user)
    email = request.form['username']
    user_in_db = User.query.filter_by(account=email).first()

    if user_in_db and  request.form['password'] == user_in_db.get_password():
        flask_login.login_user(user_in_db)
        return redirect(url_for('login.protected'))
    return 'Bad login'


@bp.route('/protected')
@flask_login.login_required
def protected():
    print(flask_login.current_user)
    return 'Logged in as: ' + flask_login.current_user.account


@bp.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'