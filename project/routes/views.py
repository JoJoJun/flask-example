# import flask_login
from project.models.model import User, SentTable, Switch, BgImage
from flask import Flask, redirect, url_for,render_template,request,Blueprint, jsonify, send_from_directory,make_response
from project.models import db
import os
import time
import random
from sqlalchemy import func
from project.services.utils import get_logo_switch, get_max_id, get_min_id, get_all_text, get_all_bgs

bp = Blueprint('home', __name__, url_prefix='/')
basedir = os.path.dirname(os.path.dirname(__file__))

@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('helloworld.html')


@bp.route('/all_counts', methods=['GET', 'POST'])
def get_all_count():
    print("get all text")
    sent_in_db = SentTable.query.count()
    print(sent_in_db)
    bg_in_db = db.session.query(BgImage).count()
    print("bg image:", bg_in_db)
    return jsonify({
        'status': 0,
        'sentsAll': sent_in_db,
        'all_bgs':bg_in_db
    })
    # return render_template('helloworld.html')
@bp.route('/sent_counts', methods=['GET', 'POST'])
def get_sent_count():
    print("get all text")
    sent_in_db = SentTable.query.count()
    print(sent_in_db)
    return jsonify({
        'status': 0,
        'sentsAll': sent_in_db,
    })
# add a sent
@bp.route('/add_sent', methods=[ 'POST'])
def add_sent():
    data = request.get_json(silent=True)
    sent = data['sent']
    print("get sent:", sent)
    sent_session = SentTable.query.filter_by(sent=sent).first()
    res = {}
    status = 0
    if sent_session:
        msg = '句子已经存在'
        res['msg'] = msg
        res['status'] = 1
        return jsonify(res)
    else:
        new_sent = SentTable(sent = sent)
        try:
            db.session.add(new_sent)
            db.session.flush()
            db.session.commit()
            print("id=", new_sent.id)
            msg = '添加成功'
        except :
            msg = "add error"
            status = 1
        res['msg'] = msg
        res['status'] = status
        return jsonify(res)
        # return redirect(url_for('login.login'))
    # return redirect(url_for('login.login'))

# delete a sent
@bp.route('/del_sent', methods=[ 'POST'])
def delete_sent():
    data = request.get_json(silent=True)
    id = data['id']
    print("get id:", id)
    # sent_session = SentTable.query.filter_by(sent=sent).first()
    # sent_session = db.session.query(SentTable).filter_by(id=id).first()
    sent_session = db.session.query(SentTable).get(id)
    print(sent_session)
    res = {}
    status = 0
    if not sent_session:
        msg = '句子ID不存在'
        res['msg'] = msg
        res['status'] = 1
        return jsonify(res)
    else:
        try:
            db.session.delete(sent_session)
            db.session.commit()
            msg = '删除成功'
        except Exception as e:
            msg = "delete error"
            status = 1
            print(e)
        res['msg'] = msg
        res['status'] = status
        return jsonify(res)

@bp.route('/image_page', methods=['GET', 'POST'])
def get_image_per_page():
    if request.method == 'GET':
        page = 1
        page_num = 10
        # TODO 返回第一页数据
        pass
    page = request.form['page_num']
    page_num = request.form['page_num']
    print("page={}, pahenum={}".format(page, page_num))
    paginate = BgImage.query.paginate(page, page_num, False)
    print("get all text")
    # sent_in_db = SentTable.query.limit(10).all()
    print(len(paginate))
    data = []
    for obj in paginate:
        d = {}
        d['sent'] = obj.sent
        print(obj.sent)
        data.append(d)
    # return data
    return jsonify(data)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@bp.route('/add_image', methods=['GET','POST'])
def add_image():
    data = request.get_json(silent=True)
    img = request.files.get('photo')
    res = {}
    # check name and style
    if not allowed_file(img.filename):
        res["msg"] = "图片格式不符合要求，只允许'png', 'jpg', 'JPG', 'PNG'后缀"
        return render_template('images.html', msg=res)
    name = str(int(time.time()))+"_"+img.filename
    img.filename = name
    print(name)
    # path = basedir+"/static/pictures/"
    # path = basedir + "\\"
    path = os.path.join(basedir, "static")
    path = os.path.join(path, "pictures")
    file_path = os.path.join(path, img.filename)
    print(file_path)
    img.save(file_path)
    # 存到数据库
    status = 0
    img_session = db.session.query(BgImage).filter_by(p_name=name).first()
    if img_session:
        msg = '图片已经存在'
        res['msg'] = msg
        res['status'] = 1
        return jsonify(res)
    else:
        new_img = BgImage(file_ID=file_path, p_name=name)
        try:
            db.session.add(new_img)
            # db.session.flush()
            db.session.commit()
            # print("id=", new_img.id)
            msg = '添加成功'
        except:
            msg = "add error"
            status = 1
        res['msg'] = msg
        res['status'] = status
    print("upload sucess")
    return jsonify(res)
    # add to sql
    # return render_template('images.html', msg=res)

@bp.route('/download/<string:filename>', methods=['GET'])
def download(filename):
    if request.method == "GET":
        path = os.path.join(basedir, "static")
        path = os.path.join(path, "pictures")
        if os.path.isfile(os.path.join(path, filename)):
            return send_from_directory(path, filename, as_attachment=True)
        pass

# show photo
@bp.route('/show/<string:filename>', methods=['GET'])
def show_photo(filename):
    file_dir = os.path.join(basedir, app.config['UPLOAD_FOLDER'])
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open(os.path.join(file_dir, '%s' % filename), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass

# delete photo
@bp.route('/del_photo', methods=['GET','POST'])
def delete_photo():
    name = request.form.get("pic_name")
    print("get name:", name)
    # 查询路径
    res = {}
    img_session = db.session.query(BgImage).filter_by(p_name=name).first()
    if img_session:
        file = img_session.file_ID
        print("file=",file)
        delete_ok = False
        try:
            db.session.delete(img_session)
            db.session.commit()
            msg = '删除成功'
            delete_ok = True
        except Exception as e:
            msg = "delete error"
            print(e)
        if delete_ok:
            # 删除文件
            os.remove(file)
            msg = '已删除'
            res['msg'] = msg
        return jsonify(res)
    else:
        msg = '图片不存在'
        res['msg'] = msg
        return jsonify(res)

@bp.route('/get_random_sents', methods=['GET', 'POST'])
def get_random_sents():
    num = request.form.get("num")
    print("num", num)
    num = int(num)
    # 查询cnt
    # sent_in_db = db.session.query(SentTable).count()
    # 最大的ID
    sent_min = db.session.query(SentTable)
    # res_max = db.session.query(func.max(SentTable.id).label('id')).one()
    max_id = get_max_id(SentTable)
    # maxs = db.session.query(func.max(SentTable.id)).first()
    print(max_id)
    min_id = get_min_id(SentTable)
    # 最小的ID
    # res_min = db.session.querry(func.min(SentTable.id)).lable('id').one
    print("here id",min_id, max_id)
    # 随机数不超过count
    res = {}
    sent_list = []
    cnt = 0
    while cnt < num:
        randid = random.randint(min_id,max_id)
        # cnt += 1
        sent_session = db.session.query(SentTable).get(randid)
        if sent_session and sent_session.sent:
            sent_list.append(sent_session.sent)
            print(sent_session.sent)
            cnt += 1
    res['sents'] = sent_list
    return jsonify(res)


# 查询随机图片 主要是怎么返回给小程序


# 查logo状态
@bp.route('/get_switch', methods=['GET', 'POST'])
def get_switch_value():
    print("get logo switch")
    data = request.get_json(silent=True)
    switch_name = data['switch_name']
    print("get switch name:", switch_name)
    # switch_in_db = Switch.query.filter_by(switch_name = switch_name).first()
    switch_value = get_logo_switch(switch_name)
    # print(switch_in_db.switch_value)
    print("swicth value:", switch_value)
    res = {}
    res['status'] = 0
    res['switch_value'] = True if switch_value == 1 else False
    return jsonify((res))

# change logo状态
@bp.route('/change_switch', methods=['GET', 'POST'])
def change_switch_value():
    print("change  logo switch")
    data = request.get_json(silent=True)
    switch_name = data['switch_name']
    switch_value = data['switch_value']
    print("here swicth_value:",switch_value)
    try:
        logo_session = db.session.query(Switch).filter_by(switch_name=switch_name).first()
        logo_session.switch_value = switch_value
        # 提交会话
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            'status':1,
            'msg': '修改失败'
        })
    return jsonify({
        'status':0,
        'msg':'修改成功，当前状态为：'+ str(switch_value)
    })

@bp.route('/get_all_text', methods=['GET','POST'])
def get_text():
    data = request.get_json(silent=True)
    print("data", data)
    page_size = data['pageSize']
    page = data['page']
    table_data = get_all_text(page_size, page)
    # sents_all = sents_all[:20]
    if not table_data:
        return jsonify({
            'status': 1,
            'msg': '未知错误'
        })
    return jsonify({
        'status': 0,
        'sents_all': table_data,
    })

@bp.route('/get_all_bgs', methods=['GET','POST'])
def get_bgs():
    data = request.get_json(silent=True)
    print("data", data)
    page_size = data['pageSize']
    page = data['page']
    table_data = get_all_bgs(page_size, page)
    # sents_all = sents_all[:20]
    if not table_data:
        return jsonify({
            'status': 1,
            'msg': '未知错误'
        })
    return jsonify({
        'status': 0,
        'bgs_all': table_data,
    })