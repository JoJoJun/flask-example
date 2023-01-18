import flask_login
from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint,jsonify,make_response
from datetime import datetime
from project.models import db
## 登录的路由和逻辑都在这页了
login_bp = Blueprint('login', __name__, url_prefix='/account')
login_manager = flask_login.LoginManager()

@login_bp.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin']='*'
    environ.headers['Access-Control-Allow-Method']='*'
    environ.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return environ

@login_bp.route('/',methods=['GET', 'POST'])
def index():
    print('in index')
    return render_template('helloworld.html')
# users = {'foo@bar.tld': {'password': 'secret'}}
@login_manager.user_loader
def load_user(account):
    return User.query.get(account)


# @login_bp.route('/login/', methods=['GET', 'POST'])
# def login():
#     print("in login!!!!!")
#     if request.method == 'GET':
#         return render_template('helloworld.html',user=flask_login.current_user)
#     data = request.get_json(silent=True)
#     print(data)
#     email = data['username']
#     password = data['password']
#     # email = request.form['username']
#     # password = request.form['password']
#     print(email, password)
#     print("here password:", pasw)
#     user_in_db = User.query.filter_by(user_name=email).first()
#     print(user_in_db.password)
#     res = {}
#     if not user_in_db:
#         msg = '用户不存在'
#         res['msg'] = msg
#         return jsonify(res)
#         # return render_template('helloworld.html',msg = msg)
#     elif password != user_in_db.password:
#         msg='密码错误'
#         res['msg'] = msg
#         return jsonify(res)
#         # return render_template('helloworld.html',msg = msg)
#     if user_in_db and request.form['password'] == user_in_db.password:
#         # flask_login.login_user(user_in_db)
#         msg = "成功"
#         res['msg'] = msg
#         res = make_response(jsonify(res))
#         res.headers['Access-Control-Allow-Origin'] = '*'
#         res.headers['Access-Control-Allow-Method'] = '*'
#         res.headers['Access-Control-Allow-Headers'] = '*'
#         return res
        #
@login_bp.route('/login/',methods=['GET', 'POST'],strict_slashes=False)
def login():
    print('in login')
    data = request.get_json(silent=True)
    print("data",data)
    username = data['username']
    password = data['password']
    # username = request.form['username']
    # password = request.form['password']
    user_in_db = User.query.filter_by(user_name=username).first()
    print(user_in_db)
    if not user_in_db:
            msg = '用户或密码不正确'
            return jsonify({
                'status':1,
                'msg':msg
            })
    elif password != user_in_db.password:
            msg='用户或密码不正确'
            return jsonify({
                'status': 1,
                'msg': msg
            })
    if user_in_db and  password == user_in_db.password:
            # flask_login.login_user(user_in_db)
            # print("current user:{}".format(flask_login.current_user.name))
            return jsonify({
                'status': 0,
                'msg': '登录成功！',
                'token':'123'
            })
    return jsonify({
        'status': 2,
        'msg': '未知错误'
    })


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
    user_name = request.form['email']
    print(username,password,password_confum,user_name)
    user = User.query.filter_by(user_name=user_name).first()
    if user:
        msg = '账户已注册'
        return render_template('regist.html',msg=msg)
    elif password != password_confum:
        msg = '确认密码错误，请重新输入'
        return render_template('regist.html', msg=msg)
    else:
        dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_user = User(user_name=user_name, password=password)
        db.session.add(new_user)
        db.session.commit()
        msg = '注册成功'
        return redirect(url_for('login.login'))
    return redirect(url_for('login.login'))


@login_bp.route('/logout/')
def logout():
    flask_login.logout_user()
    return 'Logged out'