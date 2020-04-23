# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, MetaData, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy


engine = create_engine('mysql+pymysql://root:password@localhost/database_name', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
metadata = Base.metadata
Base.query = db_session.query_property()
db = SQLAlchemy()



class User(Base):
    __tablename__ = 'user'

    account = Column(String(255), primary_key=True, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), server_default=FetchedValue())
    vip_flag = Column(Integer, nullable=False, server_default=FetchedValue())
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    state = Column(Integer)

    def __init__(self, email,password,name,create_time,update_time):
        self.account = email
        self.password = password
        self.name = name
        self.vip_flag = 1
        self.create_time = create_time
        self.update_time = update_time
        self.state = 1

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
