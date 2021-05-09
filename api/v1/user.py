#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: user.py
"""

# base
import sqlalchemy.exc
from flask_restx import Namespace, Resource, reqparse, fields

# serializer
import serializer
from model import db
from model.user import User as UserModel

user_namespace = Namespace("user", description="用户路由")


# UserRegister 用户注册
@user_namespace.route("/register")
class UserRegister(Resource):
    # userDataSwagger 用于swagger文档显示
    userDataSwagger = user_namespace.model('userData', {
        "username": fields.String(description="用户名", required=True),
        "password": fields.String(description="密码", required=True)
    })

    @user_namespace.doc(body=userDataSwagger)
    def post(self):
        """
        添加用户
        :return: serializer.Response
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username', location="json")
        parser.add_argument('password', type=str, help='Password', location="json")
        args = parser.parse_args()

        username = args.get("username", None)
        password = args.get("password", None)

        if (username is None) or (password is None):
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "用户名或密码输入不合法").Return()

        try:
            user = UserModel().create(username, password)
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return serializer.Response(serializer.USER_INPUT_ERROR, e.args, "用户创建失败!").Return()

        return serializer.Response(0, None, "用户创建成功!").Return()


# 用户登录
@user_namespace.route("/login")
class UserLogin(Resource):
    def post(self):
        """
        用户登录
        :return:
        """
        pass
