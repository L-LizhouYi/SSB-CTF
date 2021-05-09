#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: user.py
"""

import bcrypt

from model import db


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

    # setPassword 设置密码 传入明文需要加密成慢哈希
    def setPassword(self, password):
        salt = bcrypt.gensalt(5)
        return bcrypt.hashpw(password.encode("utf-8"), salt)

    def create(self, username, password):
        self.username = username
        self.password = self.setPassword(password)
        return self
