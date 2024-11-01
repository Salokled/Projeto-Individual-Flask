import os

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///sge_py.db'
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/sge_py'
    SQLALCHEMY_TRACK_MODIFICATIONS = False