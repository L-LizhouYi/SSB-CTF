# SSB-CTF (一个极简的CTF平台)
## 开发进度
- [x] 用户注册
- [ ] 验证码
- [ ] 用户登录
- [ ] 获取用户信息
- [ ] JWT续约

## 技术栈
- [Flask](https://github.com/pallets/flask)
- [Flask-restx](https://github.com/python-restx/flask-restx)
- [Flask-SQLalchemy](https://github.com/pallets/flask-sqlalchemy)

## 目录结构
- `api/` 用来存放api的路由和处理函数
- `middleware/` 用来存放自定义的中间件
- `server/` 服务器核心, 变量配置都在这里
- `main.py` 服务器入口文件
- `.env` 环境变量文件
- `requirements.txt` 依赖模块

## 使用
```
pip install -r requirements.txt
python main.py
```

### 开发者
- [Hel1antHu5](https://github.com/L-HeliantHuS)
- [@TGDD](https://github.com/NefertariTim)