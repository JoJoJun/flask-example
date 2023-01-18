# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, MetaData, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
import datetime

engine = create_engine('mysql+pymysql://root:congxinzhiyu1?@49.235.89.185/congxinzhiyu_xcx', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
metadata = Base.metadata
Base.query = db_session.query_property()
db = SQLAlchemy()

class BgImage(Base):
    __tablename__ = 'bg_images'

    id = Column(BigInteger, primary_key=True)
    file_ID = Column(String(255), primary_key=True, nullable=False)
    p_name = Column(String(255), nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now)

    def __init__(self, file_ID, p_name):
        self.file_ID = file_ID
        self.p_name = p_name


class SentTable(Base):
    __tablename__ = 'sent_table'

    id = Column(BigInteger, primary_key=True)
    sent = Column(String(555))
    create_time = Column(DateTime,default=datetime.datetime.now)
    def __init__(self, sent):
        self.sent = sent

    def get_sent(self):
        return self.sent


class Switch(Base):
    __tablename__ = 'switch'

    id = Column(Integer, primary_key=True)
    switch_name = Column(String(255), nullable=False)
    switch_value = Column(Integer)
    def __init__(self, switch_name,switch_value):
        self.switch_name = switch_name
        self.switch_value = switch_value



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    def __init__(self, user_name,password):
        self.user_name = user_name
        self.password = password




# class User(Base):
#     __tablename__ = 'user'
#
#     account = Column(String(255), primary_key=True, unique=True)
#     password = Column(String(255), nullable=False)
#     name = Column(String(255), server_default=FetchedValue())
#     vip_flag = Column(Integer, nullable=False, server_default=FetchedValue())
#     create_time = Column(DateTime)
#     update_time = Column(DateTime)
#     state = Column(Integer)
#
#     def __init__(self, email,password,name,create_time,update_time):
#         self.account = email
#         self.password = password
#         self.name = name
#         self.vip_flag = 1
#         self.create_time = create_time
#         self.update_time = update_time
#         self.state = 1
#
#     def is_authenticated(self):
#         return True
#
#     def is_active(self):
#         return True
#
#     def is_anonymous(self):
#         return False
#
#     def get_id(self):
#         return self.account
#
#     def get_password(self):
#         return self.password
#
#     def __repr__(self):
#         return '<User %r>' % (self.name)
