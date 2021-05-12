#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-12
@ FileName: util.py
"""
from model.user import User
from model import db
import getpass

def createSuperUser():
    email = input("email:")
    username = input("username (default: root):")

    if username == "":
        username = "root"

    password = getpass.getpass("password (required):")

    user = User().create(username, password, email=email, is_admin=True)
    db.session.add(user)
    db.session.commit()

    print(f"创建管理员{user.username}成功!")