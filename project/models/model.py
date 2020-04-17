# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Integer, MetaData, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('mysql+pymysql://DaaS:flask2020@39.97.219.243/daas', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
metadata = Base.metadata
Base.query = db_session.query_property()


class File(Base):
    __tablename__ = 'file'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    type = Column(Integer)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    state = Column(Integer)



class Model(Base):
    __tablename__ = 'model'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    algorithm = Column(String(255))
    RTengine = Column(String(255))
    description = Column(String(255))
    version = Column(Integer)
    assessment = Column(String(255))
    file = Column(ForeignKey('file.id'), nullable=False, index=True)
    project = Column(ForeignKey('project.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    state = Column(Integer)

    file1 = relationship('File', primaryjoin='Model.file == File.id', backref='models')
    project1 = relationship('Project', primaryjoin='Model.project == Project.id', backref='models')



class Project(Base):
    __tablename__ = 'project'

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    route = Column(String(255), nullable=False)
    description = Column(String(255))
    user = Column(ForeignKey('user.account', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    state = Column(Integer)

    user1 = relationship('User', primaryjoin='Project.user == User.account', backref='projects')



class Record(Base):
    __tablename__ = 'record'

    id = Column(BigInteger, primary_key=True)
    model = Column(ForeignKey('model.id'), nullable=False, index=True)
    url = Column(String(255), nullable=False)
    RTenvironment = Column(String(255))
    cpu = Column(Float)
    memory = Column(Float)
    load = Column(Integer, nullable=False, server_default=FetchedValue())
    create_time = Column(DateTime)
    state = Column(String(255), info='鏄?惁鍦ㄩ儴缃茬姸鎬')

    model1 = relationship('Model', primaryjoin='Record.model == Model.id', backref='records')



class User(Base):
    __tablename__ = 'user'

    account = Column(String(255), primary_key=True, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(255), server_default=FetchedValue())
    vip_flag = Column(Integer, nullable=False, server_default=FetchedValue())
    create_time = Column(DateTime)
    update_time = Column(DateTime)
    state = Column(Integer)

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
