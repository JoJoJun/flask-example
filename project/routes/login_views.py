import flask_login
from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint
from datetime import datetime
from project.models import db
## 登录的路由和逻辑都在这页了
login_bp = Blueprint('login', __name__, url_prefix='/account')
login_manager = flask_login.LoginManager()

@login_bp.route('/',methods=['GET', 'POST'])
def index():
    print('in index')
    return render_template('helloworld.html')
# users = {'foo@bar.tld': {'password': 'secret'}}
@login_manager.user_loader
def load_user(account):
    return User.query.get(account)


@login_bp.route('/login/', methods=['GET', 'POST'])
def login():
    print("in login!!!!!")
    if request.method == 'GET':
        return render_template('helloworld.html',user=flask_login.current_user)
    email = request.form['username']
    password = request.form['password']
    user_in_db = User.query.filter_by(account=email).first()
    print(user_in_db)
    if not user_in_db:
        msg = '用户不存在'
        return render_template('helloworld.html',msg = msg)
    elif password != user_in_db.get_password():
        msg='密码错误'
        return render_template('helloworld.html',msg = msg)
    if user_in_db and  request.form['password'] == user_in_db.get_password():
        flask_login.login_user(user_in_db)
        return redirect(url_for('login.protected'))


@login_bp.route('/protected')
@flask_login.login_required
def protected():
    print(flask_login.current_user)
    return 'Logged in as: ' + flask_login.current_user.account


@login_bp.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html', user=flask_login.current_user)
    username = request.form['username']
    password = request.form['password']
    password_confum = request.form['password_confum']
    email = request.form['email']
    print(username,password,password_confum,email)
    user = User.query.filter_by(account=email).first()
    if user:
        msg = '账户已注册'
        return render_template('regist.html',msg=msg)
    elif password != password_confum:
        msg = '确认密码错误，请重新输入'
        return render_template('regist.html', msg=msg)
    else:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = User(email=email, password=password, name=username, create_time=dt, update_time=dt)
        db.session.add(new_user)
        db.session.commit()
        msg = '注册成功'
        return redirect(url_for('login.login'))
    return redirect(url_for('login.login'))


@login_bp.route('/logout/')
def logout():
    flask_login.logout_user()
    return 'Logged out'