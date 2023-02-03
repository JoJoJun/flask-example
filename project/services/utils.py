from project.models.model import User, SentTable, Switch, BgImage
from project.models import db
from sqlalchemy import func

# get logo status
def get_logo_switch(switch_name):
    switch_in_db = Switch.query.filter_by(switch_name=switch_name).first()
    print(switch_in_db.switch_value)
    return switch_in_db.switch_value

# get min ID
def get_min_id(table):
    print("here in get min id")
    res = db.session.query(func.min(table.id)).first()
    print(res[0])
    return res[0]

# get max ID
def get_max_id(table):
    print("here in get max id")
    res = db.session.query(func.max(table.id)).first()
    print(res[0])
    return res[0]

# 查询所有文本
def get_all_text(page_size, page):
    sents_all =  db.session.query(SentTable).order_by(SentTable.id.desc()).paginate(page=page, per_page=page_size, error_out=False)
    # print(sents_all,type(sents_all))
    # print(sents_all.items, type(sents_all.items))
    table_data = []
    for sent in sents_all.items:
        print(sent.id)
        dic = {}
        dic['date'] = sent.create_time.strftime("%Y-%m-%d")
        dic['text'] = sent.sent
        dic['id'] = sent.id
        table_data.append(dic)
    # print(table_data)
    # total = SentTable.query.count()
    # print("total_num:{}".format(total))
    return table_data

# 查询所有文本
def get_all_bgs(page_size, page):
    bgs_all =  db.session.query(BgImage).order_by(BgImage.id.desc()).paginate(page=page, per_page=page_size, error_out=False)
    # print(sents_all,type(sents_all))
    # print(sents_all.items, type(sents_all.items))
    table_data = []
    for bg in bgs_all.items:
        dic = {}
        src_all = bg.file_ID
        src_list = src_all.split("assets")
        # if len(src_list) >= 2:
        # path = src_list[1]
        # TODO 这里上服务器需要改
        path = src_all
        # print(path)
        # path = "/".join(path.split("\\"))
        # print(path)
        dic["path"] = path
        dic["img"] = "require(" + "@/assets/" + path + ")"
        print(dic["img"])
        dic['date'] = bg.create_time.strftime("%Y-%m-%d")
        dic['id'] = bg.id
        table_data.append(dic)
    print(len(table_data))
    # total = SentTable.query.count()
    # print("total_num:{}".format(total))
    return table_data
# 合成图片
