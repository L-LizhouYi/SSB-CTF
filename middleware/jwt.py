#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-11
@ FileName: jwt.py
"""
import flask_jwt_extended.exceptions
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request, get_jwt
from functools import wraps
from cache import redisClient
import serializer

jwt = JWTManager()

# jwt不正确回调函数 自定义
@jwt.invalid_token_loader
def my_invalid_token(error):
    return serializer.Response(serializer.JWT_TOKEN_ERROR, None, "JWT TOKEN 不正确！").Return()


# jwt过期回调函数 自定义
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return serializer.Response(serializer.JWT_TOKEN_ERROR, None, "JWT已过期, 请重新登录.").Return()


# login_required 需要登录
def login_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional=True)
            if get_jwt() == {}:
                return serializer.Response(serializer.JWT_FORMAT_ERROR, None, "JWT TOKEN未填写").Return()

            if (checkJWTisLogout(get_jwt()["jti"])):
                return serializer.Response(serializer.JWT_EXPIRED_ERROR, None, "token已失效").Return()

            return fn(*args, **kwargs)
        return decorator
    return wrapper

# admin_required 需要是管理员
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request(optional=True)
            if get_jwt() == {}:
                return serializer.Response(serializer.JWT_FORMAT_ERROR, None, "JWT TOKEN未填写").Return()

            if (checkJWTisLogout(get_jwt()["jti"])):
                return serializer.Response(serializer.JWT_EXPIRED_ERROR, None, "token已失效").Return()

            claims = get_jwt_identity()
            if claims["is_admin"]:
                return fn(*args, **kwargs)
            else:
                return serializer.Response(serializer.JWT_TOKEN_ERROR, None, "您不是管理员").Return()
        return decorator
    return wrapper

# checkJWTisLogout 检查jwt是否已经被注销过了
def checkJWTisLogout(jwt_uuid):
    return redisClient.sismember("jwt:black", jwt_uuid)