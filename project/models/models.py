# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Index, Integer, MetaData, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
metadata = Base.metadata
db = SQLAlchemy()
db.Model.metadata.reflect(db.engine)

class File(db.Model):
    __tablename__ = 'file'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    path = Column(String(50), nullable=False)
    type = Column(Integer, nullable=False, info='模型文件or数据集')
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    state = Column(Integer, nullable=False, info='0:normal  -1:deleted')



class Model(db.Model):
    __tablename__ = 'model'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(Integer, nullable=False)
    algorithm = Column(String(50), nullable=False)
    RTengine = Column(String(50), nullable=False)
    description = Column(String(50))
    assessment = Column(String(50))
    version = Column(Integer, nullable=False)
    project = Column(ForeignKey('project.id'), nullable=False, index=True)
    file = Column(ForeignKey('file.id'), nullable=False, index=True)
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    state = Column(Integer, nullable=False, info='0:normal -1:deleted')

    file1 = relationship('File', primaryjoin='Model.file == File.id', backref='models')
    project1 = relationship('Project', primaryjoin='Model.project == Project.id', backref='models')



class Project(db.Model):
    __tablename__ = 'project'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), nullable=False)
    route = Column(String(50), nullable=False)
    description = Column(String(50))
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    state = Column(Integer, nullable=False, info='0:normal -1:deleted')
    user = Column(ForeignKey('user.account'), nullable=False, index=True)

    user1 = relationship('User', primaryjoin='Project.user == User.account', backref='projects')



class Record(db.Model):
    __tablename__ = 'record'

    id = Column(BigInteger, primary_key=True)
    model = Column(ForeignKey('model.id'), nullable=False, index=True)
    model_url = Column(String(100), nullable=False)
    RTenvironment = Column(String(100))
    cpu = Column(Float(asdecimal=True), nullable=False, info='0:不预留  -1：预留')
    memory = Column(Float(asdecimal=True), nullable=False)
    load = Column(Integer, info='提供web服务的负载均衡 缺省值为1')
    create_time = Column(DateTime, nullable=False)
    state = Column(Integer, nullable=False, info='0:not yet  1:ing')

    model1 = relationship('Model', primaryjoin='Record.model == Model.id', backref='records')



class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        Index('account', 'account', 'password', 'name', 'vip_flag', 'create_time', 'update_time', 'state'),
    )

    account = Column(String(50), primary_key=True, info='账号')
    password = Column(String(50), nullable=False)
    name = Column(String(50), info='用户名\\r\\n')
    vip_flag = Column(Integer, info='0:yes 1:no')
    create_time = Column(DateTime, nullable=False)
    update_time = Column(DateTime)
    state = Column(Integer, nullable=False, info='0:normal  -1:deleted')

    def __init__(self, email):
        self.email = email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.account

    def get_password(self):
        return self.password

    def __repr__(self):
        return '<User %r>' % (self.name)
