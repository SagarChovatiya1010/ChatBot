import json

from bson import ObjectId, json_util
from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


app = Flask(__name__)
uri = "mongodb+srv://sagarchovatiya0104:sagarchovatiya0104@cluster0.onof6ue.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongodb_client.db


class User(object):
    def __init__(self, _id, name, age):
        self.id = _id
        self.name = name
        self.age = age

    def __str__(self):
        return "{0} ,{1}, {2}".format(self.id, self.name, self.age)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        id = request.args.get('name')
        response = db.chatbot.find({'name': id})
        for res in response:
            usr = User(**res)
            print(usr)
            return "success"
    if request.method == "POST":
        name = request.args.get('name')
        age = request.args.get('age')
        db.chatbot.insert_one({
            "name": name,
            "age": age
        })
        print(name, age)
    return "success"


if __name__ == '__main__':
    print("start")
    print(mongodb_client.db)
    app.run()