from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
from datetime import timedelta

app = Flask(__name__, template_folder='../templates')
app.config["MONGO_URI"] = "mongodb://localhost:27017/oppo"
app.config.update(
    JWT_SECRET_KEY="luobiyunyan",
    JWT_EXPIRATION_DELTA=timedelta(seconds=3600 * 48),
    JWT_VERIFY_CLAIMS=['signature', 'exp', 'iat'],
    JWT_REQUIRED_CLAIMS=['exp', 'iat'],
    JWT_AUTH_ENDPOINT='jwt',
    JWT_ALGORITHM='HS256',
    JWT_LEEWAY=timedelta(seconds=10),
    JWT_AUTH_HEADER_PREFIX='JWT',
    JWT_NOT_BEFORE_DELTA=timedelta(seconds=0)
)
mongo = PyMongo(app)
