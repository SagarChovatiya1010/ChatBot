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
# app.config["SECRET_KEY"] = "3c323796460665ffb44cf595a11bc8fa97f0433f"
# app.config["MONGO_URI"] = "mongodb+srv://sagarchovatiya0104:sagarchovatiya0104@cluster0.onof6ue.mongodb.net/?retryWrites=true&w=majority"


# mongodb_client = PyMongo(app)
db = mongodb_client.db


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        id = request.args.get('name')
        response = db.chatbot.find({'name': id})
        # response = db.chatbot.find()
        for res in response:
            print(res)
            res = {
                'name' : res['name'],
                'age': res['age']
            }
            return res
        # print(response)
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