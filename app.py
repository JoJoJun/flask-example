import project
# from flask import Flask, redirect, url_for,render_template,request
# import flask_login
# from models.models import User
# # Flask构造函数使用当前模块（__name __）的名称作为参数。
# app = Flask(__name__)
# login_manager = flask_login.LoginManager()
# login_manager.init_app(app)
#
#
# # Flask类的route()函数是一个装饰器，它告诉应用程序哪个URL应该调用相关的函数。
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# users = {'foo@bar.tld': {'password': 'secret'}}
# @login_manager.user_loader
# def load_user(account):
#     return User.query.get(account)
# #
# # @login_manager.request_loader
# # def request_loader(request):
# #     email = request.form.get('email')
# #     if email not in users:
# #         return
# #     user = User()
# #     user.id = email
# #
# #     # DO NOT ever store passwords in plaintext and always compare password
# #     # hashes using constant-time comparison!
# #     user.is_authenticated = request.form['password'] == users[email]['password']
# #
# #     return user
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('helloworld.html')
#     email = request.form['email']
#     user_in_db = User.query.filter_by(account=email).first()
#
#     if user_in_db and  request.form['password'] == user_in_db.get_password():
#         flask_login.login_user(user_in_db)
#         return redirect(url_for('protected'))
#     return 'Bad login'
#
# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     print(flask_login.current_user)
#     return 'Logged in as: ' + flask_login.current_user.account
# @app.route('/logout')
# def logout():
#     flask_login.logout_user()
#     return 'Logged out'
#
# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'
# @app.route('/hello')
# def hello_world2():
#    return render_template('helloworld.html')
#
#
# # 可以在url中添加参数
# @app.route('/hello/<name>')
# def hello_name(name):
#    return 'Hello %s!' % name
#
#
# @app.route('/rev/<float:revNo>')
# # 换成整数会404
# def revision(revNo):
#    return 'Revision Number %f' % revNo
#
#
# # url_for 动态返回不同的函数 重定向 注意guset 和user url后面都要跟上参数的
# @app.route('/admin')
# def hello_admin():
#    return 'Hello Admin'
#
#
# @app.route('/guest/<guest>')
# def hello_guest(guest):
#    return 'Hello %s as Guest' % guest
#
#
# @app.route('/user/<name>')
# def hello_user(name):
#    if name =='admin':
#       return redirect(url_for('hello_admin'))
#    else:
#       return redirect(url_for('hello_guest',guest = name))
#
#
if __name__ == '__main__':
    # app.run(host, port, debug, options)
    # host要监听的主 机名。 默认为127.0.0.1（localhost）
    # debug 默认为false。 如果设置为true，则提供调试信息   options 要转发到底层的Werkzeug服务器
    app = project.create_app()
    app.run(debug=True)
