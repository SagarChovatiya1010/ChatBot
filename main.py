import json

from bson import ObjectId, json_util
from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.models.add_data import AddData
from src.models.bot import Bot
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


@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == "POST":
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            req = request.json
            data = AddData(**req)
            bots = db.bot.find({'bot_id': data.bot_id})
            bot_count = 0
            for bot in bots:
                bot_count = bot_count + 1
            if bot_count == 0:
                print("bot not present")
                db.bot.insert_one({"bot_id": data.bot_id, "bot_name": data.bot_name})
                # print(data.bot_steps)
                for key in data.bot_steps:
                    # print(key, data.bot_steps[key])
                    db.bot_steps.insert_one({"step_id": key, "next_steps": data.bot_steps[key]})
            else:
                return "bot already present"
            return "success"
        else:
            return 'Content-Type not supported!'


if __name__ == '__main__':
    app.run()