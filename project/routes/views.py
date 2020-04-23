import flask_login
from project.models.model import User
from flask import Flask, redirect, url_for,render_template,request,Blueprint
## 登录的路由和逻辑都在这页了
bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('helloworld.html')