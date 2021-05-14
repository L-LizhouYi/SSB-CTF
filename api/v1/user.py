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

        if ( (username is None) or (password is None) or (email is None) ) and ( 18 < len(username) < 4 ):
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "输入参数不合法 (可能是用户名长度不正确哦.)").Return()

        # 检查用户名是否存在
        temp = UserModel.query.filter_by(username=username).first()
        if temp is not None:
            return serializer.Response(serializer.USER_EXIST_ERROR, None, "用户名已存在").Return()

        # 检查邮箱是否已经被注册
        temp = UserModel.query.filter_by(email=email).first()
        if temp is not None:
            return serializer.Response(serializer.USER_EXIST_ERROR, None, "该邮箱已被使用").Return()

        # 防止写入数据库出错.
        try:
            user = UserModel().create(username=username, password=password, email=email, is_admin=False)
            db.session.add(user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            return serializer.Response(serializer.SERVER_DATABASE_ERROR, e.args, "用户创建失败!").Return()

        return serializer.Response(0, None, "用户创建成功!").Return()


# 用于swagger文档显示
userLoginDataSwagger = user_namespace.model('userLoginData', {
    "username": fields.String(description="用户名", required=True),
    "password": fields.String(description="密码", required=True)
})

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
        parser.add_argument('email', type=str, help='Email', location="json")
        args = parser.parse_args()

        username = args.get("username", None)
        password = args.get("password", None)
        email = args.get("email", None)

        if ((username is None) and (email is None)) or (password is None):
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "参数输入不合法").Return()

        if email is not None:
            user = UserModel.query.filter_by(email=email).first()
        else:
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


# UserLogout 用户注销
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


userVerifyDataSwagger = user_namespace.model("userVerifyData", {
    "username": fields.String(description="用户名"),
    "email": fields.String(description="邮箱")
})

# VerifyRegistered 查看用户是否被注册
@user_namespace.route("/verify_registered")
class VerifyRegistered(Resource):
    @user_namespace.doc(body=userVerifyDataSwagger)
    def post(self):
        """
        验证用户是否存在
        可以传入username 或者 email
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, help='Username', location="json")
        parser.add_argument('email', type=str, help='Email', location="json")
        args = parser.parse_args()

        username = args.get("username", None)

        if username is not None:
            if UserModel.query.filter_by(username=username).first() is not None:
                return serializer.Response(serializer.USER_EXIST_ERROR, None, "该用户名已存在").Return()

        email = args.get("email", None)
        if UserModel.query.filter_by(email=email).first() is not None:
            return serializer.Response(serializer.USER_EXIST_ERROR, None, "该邮箱已存在").Return()

        if email is None and username is None:
            return serializer.Response(serializer.USER_INPUT_ERROR, None, "请输入内容啦~").Return()

        return serializer.Response(0, None, "该用户名或邮箱未被注册").Return()
