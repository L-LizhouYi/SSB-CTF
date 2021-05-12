#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: user.py
"""

import sqlalchemy.exc
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt, get_jwt_identity
from flask_restx import Namespace, Resource, reqparse, fields

import serializer
from middleware.jwt import login_required
from model import db
from model.user import User as UserModel
from cache import redisClient

user_namespace = Namespace("user", description="用户路由")

# 用于swagger文档显示
userRegisterDataSwagger = user_namespace.model('userRegisterData', {
    "username": fields.String(description="用户名", required=True),
    "password": fields.String(description="密码", required=True),
    "email": fields.String(description="邮箱", required=True)
})

# 用于swagger文档显示
userLoginDataSwagger = user_namespace.model('userLoginData', {
    "username": fields.String(description="用户名", required=True),
    "password": fields.String(description="密码", required=True)
})


# UserRegister 用户注册
@user_namespace.route("/register")
class UserRegister(Resource):
    @user_namespace.doc(body=userRegisterDataSwagger)
    def post(self):
        """
        添加用户
        serializer.Response
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username', location="json")
        parser.add_argument('password', type=str, help='Password', location="json")
        parser.add_argument('email', type=str, help='Email', location="json")
        args = parser.parse_args()

        username = args.get("username", None)
        password = args.get("password", None)
        email = args.get("email", None)

        if (username is None) or (password is None) or (email is None):
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "输入参数不合法").Return()

        try:
            user = UserModel().create(username=username, password=password, email=email, is_admin=False)
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return serializer.Response(serializer.USER_INPUT_ERROR, e.args, "用户创建失败!").Return()

        return serializer.Response(0, None, "用户创建成功!").Return()


# UserLogin 用户登录
@user_namespace.route("/login")
class UserLogin(Resource):
    @user_namespace.doc(body=userLoginDataSwagger)
    def post(self):
        """
        用户登录
        serializer.Response
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username', location="json")
        parser.add_argument('password', type=str, help='Password', location="json")
        args = parser.parse_args()

        username = args.get("username", None)
        password = args.get("password", None)
        if (username is None) or (password is None):
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "用户名或密码输入不合法").Return()

        user = UserModel.query.filter_by(username=username).first()
        if not user or not user.checkPassword(password):
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "用户名或密码输入不正确").Return()

        token = create_access_token(identity={
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "register_time": user.register_timed
        })

        # 返回data
        data = {
            "access_token": token,
            "token_type": "Bearer",
        }

        return serializer.Response(0, data, "登录成功!").Return()


# UserMe 获取用户信息
@user_namespace.route("/me")
class UserMe(Resource):
    @login_required()
    def get(self):
        """
        获取当前用户信息, 需要传入JWT
        serializer.Response
        """
        data = get_jwt_identity()
        return serializer.Response(0, data, "").Return()


@user_namespace.route("/logout")
class UserLogout(Resource):
    @login_required()
    def get(self):
        """
        注销用户
        serializer.Response
        """
        jwt_uuid = get_jwt()["jti"]

        redisClient.sadd("jwt:black", jwt_uuid)

        return serializer.Response(0, None, "注销成功!").Return()
