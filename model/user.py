#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: user.py
"""

import bcrypt
import time
from model import db
import datetime
from sqlalchemy.sql import func


class User(db.Model):
    """
    User 用户模型类
    id int primary key auto_increment
    username varchar(100) unique not null
    password varchar(255) not null
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    register_timed = db.Column(db.TIMESTAMP, default=func.now())

    # setPassword 设置密码 传入明文需要加密成慢哈希
    def setPassword(self, password):
        salt = bcrypt.gensalt(5)
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    # 创建用户
    def create(self, username, password, is_admin: bool):
        self.username = username
        self.password = self.setPassword(password)
        self.is_admin = is_admin
        return self

    # checkPassword 验证密码是否输入正确
    def checkPassword(self, password):
        return bcrypt.checkpw(password.encode(), self.password.encode())

    def getUserByID(self, id):
        return User.query.filter_by(id=id).first()
