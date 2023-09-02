import json

from bson import ObjectId, json_util
from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.models.add_data import AddData
from src.models.bot import Bot
from src.models.bot_execution import BotExecution
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


@app.route('/next_step', methods=['GET'])
def next_step():
    if request.method == "GET":
        cid = request.args.get('cid')
        bot_id = request.args.get('bot_id')
        command = request.args.get('command')
        responses = db.bot_execution.find({'cid': cid})
        obj = 0
        count = 0
        final_response = {}
        for r in responses:
            count = count + 1
            obj = BotExecution(**r)
        if count == 0:
            print('no customer present')
            bot_execution_obj = BotExecution(_id=123, cid=cid, bot_id=bot_id, current_step='0')
            bot_execution_obj = bot_execution_obj.__dict__
            del bot_execution_obj['_id']
            db.bot_execution.insert_one(bot_execution_obj)
            bot_steps = db.bot_steps.find({'step_id': '0'})
            for bot_step in bot_steps:
                bot_step_obj = BotSteps(**bot_step)
                final_response['message'] = bot_step_obj.step_message
                final_response['next_steps'] = []
                for every_next_step in bot_step_obj.next_steps:
                    final_response['next_steps'].append(every_next_step['criteria_value'])
            return final_response

        else:
            print('customer present')
            current_step_id = obj.current_step
            bot_steps = db.bot_steps.find({'step_id': current_step_id})
            for bot_step in bot_steps:
                bot_step_obj = BotSteps(**bot_step)
                available_next_steps = bot_step_obj.next_steps
                for every_next_step in available_next_steps:
                    if every_next_step['criteria_type'] == 'text_match':
                        criteria_value = every_next_step['criteria_value']
                        criteria_value = criteria_value.upper();
                        command = command.upper();
                        if criteria_value == command:
                            db.bot_execution.update_one({'cid': obj.cid},
                                                        {"$set": {'current_step': every_next_step['next_step_id']}})
                            next_to_next_steps = db.bot_steps.find({'step_id': every_next_step['next_step_id']})
                            for obj in next_to_next_steps:
                                next_to_next_step_obj = BotSteps(**obj)
                                final_response['message'] = next_to_next_step_obj.step_message
                                final_response['next_steps'] = []
                                for every_next_to_next_step in next_to_next_step_obj.next_steps:
                                    final_response['next_steps'].append(every_next_to_next_step['criteria_value'])
                            return final_response
                else:
                    return "enter a valid input"

    return "success"


if __name__ == '__main__':
    print(db)
    app.run()
