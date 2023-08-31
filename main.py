import json

from bson import ObjectId, json_util
from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.models.bot_steps import BotSteps

app = Flask(__name__)
uri = "mongodb+srv://sagarchovatiya0104:sagarchovatiya0104@cluster0.onof6ue.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongodb_client.db


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == "GET":
        id = request.args.get('bot_step_id')
        response = db.bot_steps.find({'bot_step_id': id})
        for res in response:
            bs = BotSteps(**res)
            response1 = db.bot_steps.find({'bot_step_id': bs.bot_next_steps[0]})
            for r in response1:
                usr2 = BotSteps(**r)
                return usr2.bot_next_steps[2]
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