from flask import render_template, jsonify, request
from app.conf._init_ import app, mongo
from bson import json_util
from werkzeug.security import check_password_hash
from app.conf.flask_jwt import jwt_required, jwt_encode, current_identity, jwt_decode
from app.conf.method import getUesrname
import time


@app.route("/")
def index():
    return render_template('index.html')


# 登录
@app.route("/api/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if len(username) == 0 or len(password) == 0:
            return jsonify(code=20,
                           msg='Please enter the correct user name or password'.encode('utf-8').decode('utf-8'))

        if mongo.db.user.find_one({"username": username}) is None:
            return jsonify(code=20, msg='user name does not exist'.encode('utf-8').decode('utf-8'))

        user_info_dict = mongo.db.user.find_one({"username": username, "password": password})  # 查询不到返回None

        if user_info_dict is None:
            return jsonify(code=22, msg='Wrong password'.encode('utf-8').decode('utf-8'))

        token = jwt_encode({'mid': str(user_info_dict['_id']), 'name': str(user_info_dict['username'])})
        return jsonify(code=10, data={'token': token.encode('utf-8').decode('utf-8')})


# jwt解码
@app.route('/api/decoder', methods=['GET', 'POST'])
def decode_token():
    if request.method == 'GET':
        return render_template('decoder.html')
    else:
        jwt_code = request.form.get('jwt')
        jwt_code_dict = jwt_decode(jwt_code)
        print(jwt_code_dict['identity']['name'])
        return jwt_code_dict


# jwt更新
@app.route('/api/token/update', methods=['POST'])
def update_token():
    jwt_code = request.form.get('jwt')
    jwt_code_dict = jwt_decode(jwt_code)
    token = jwt_encode(jwt_code_dict['identity'])
    return jsonify(code=10, data={'token': token.encode('utf-8').decode('utf-8')})


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('sign.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user_info = request.form.to_dict()
        print(user_info)
        # res = mongo.db.oppo.insert_one({"_id":1,"username": username, "password": password})
        res = mongo.db.user.insert_one(user_info)
        if res.inserted_id:
            return render_template('success.html')
        else:
            return render_template('error.html')


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('save_img.html')
    else:
        allow_formats = set(['jpeg', 'png', 'gif'])
        img = request.files.get('upload_file')
        # content = StringIO(img.read())
        # try:
        #     mime = Image.open(content).format.lower()
        #     if mime not in allow_formats:
        #         raise IOError()
        # except IOError:
        #     flask.abort(400)

        username = request.form.get("name")
        path = "C:\\Users\\30281\\Desktop\\example\\flask+mongodb2\\app\\image\\test\\"
        file_path = path + img.filename
        img.save(file_path)
        print('上传头像成功，上传的用户是：' + username)
        return render_template('success.html')


# 添加文章
@app.route("/add_article", methods=['GET', 'POST'])
def add_article():
    if request.method == 'GET':
        return render_template('add_article.html')
    else:
        token = request.form.get('token')
        title = request.form.get('title')
        description = request.form.get('description')
        imgUrl = request.form.get('imgUrl')
        username = getUesrname(token)
        current_time = time.asctime(time.localtime(time.time()))
        res = mongo.db.article.insert_one({
            "title": title, "author": username,
            "time": current_time,
            "timestamp": time.time(),
            "description": description,
            "imgUrl": imgUrl
        })
        if res.inserted_id:
            return jsonify(code=10, data={'token': token.encode('utf-8').decode('utf-8')})
        else:
            return render_template('error.html')


if __name__ == '__main__':
    app.run()
