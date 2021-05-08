#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
@ Author: HeliantHuS
@ Codes are far away from bugs with the animal protecting
@ Time:  2021-05-08
@ FileName: main.py
"""
import os
from flask import Flask
from dotenv import load_dotenv
import server

load_dotenv()

app = server.create_app()


if __name__ == '__main__':
    app.run()
