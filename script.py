from flask import Flask, request
from flask_pymongo import PyMongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.models.add_data import AddData
from src.models.bot import Bot
from src.models.bot_execution import BotExecution
from src.models.bot_steps import BotSteps
uri = "mongodb+srv://sagarchovatiya0104:sagarchovatiya0104@cluster0.onof6ue.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
mongodb_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongodb_client.db
print('script.py')
data = {
    'bot_id': '0',
    'bot_name': 'perfora',
    'bot_steps': [
        {
           'step_id': '0',
           'step_message': 'Welcome to Perfora',
           'next_steps': [
               {
                   'criteria_type': 'text_match',
                   'criteria_value': 'Shop Products',
                   'next_step_id': '1'
               },
               {
                   'criteria_type': 'text_match',
                   'criteria_value': 'Track Order',
                   'next_step_id': '2'
               },
               {
                   'criteria_type': 'text_match',
                   'criteria_value': 'Other Help',
                   'next_step_id': '3',
               }
            ]
        },
        {
           'step_id': '1',
           'step_message': 'Shop Products',
           'next_steps': [
               {
                   'criteria_type': 'text_match',
                   'criteria_value': 'Teeth',
                   'next_step_id': '4'
               },
               {
                   'criteria_type': 'text_match',
                   'criteria_value': 'Gums',
                   'next_step_id': '5'
               },
               {
                   'criteria_type': 'text_match',
                   'criteria_value': 'Bad Breath',
                   'next_step_id': '6',
               }
            ]
        },
        {
            'step_id': '2',
            'step_message': 'Track Order',
            'next_steps': [
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Order Details',
                    'next_step_id': '7'
                },
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Connect to Agent',
                    'next_step_id': '8'
                }
            ]
        },
        {
            'step_id': '3',
            'step_message': 'Other Help',
            'next_steps': [
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Cancel Order',
                    'next_step_id': '9'
                },
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Raise Issue',
                    'next_step_id': '10'
                },
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Faqs',
                    'next_step_id': '11'
                },
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Go Back',
                    'next_step_id': '0'
                }
            ]
        },
        {
            'step_id': '4',
            'step_message': 'Teeth',
            'next_steps': [
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Teeth Whitening',
                    'next_step_id': '13'
                },
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Plaque Removal',
                    'next_step_id': '14'
                }
            ]
        },
        {
            'step_id': '5',
            'step_message': 'Gums',
            'next_steps': [
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Same as Teeth',
                    'next_step_id': '-1'
                }
            ]
        },
        {
            'step_id': '6',
            'step_message': 'Bad Breath',
            'next_steps': [
                {
                    'criteria_type': 'text_match',
                    'criteria_value': 'Same as Teeth',
                    'next_step_id': '-1'
                }
            ]
        },
        {
            'step_id': '7',
            'step_message': 'Order Details are xyz',
            'next_steps': []
        },
        {
            'step_id': '8',
            'step_message': 'Connecting to agent...',
            'next_steps': []
        }
    ]
}

bots = db.bot.find({'bot_id': data["bot_id"]})
bot_count = 0
for bot in bots:
    bot_count = bot_count + 1
if bot_count == 0:
    print("bot not present")
    db.bot.insert_one({"bot_id": data["bot_id"], "bot_name": data["bot_name"]})
    # print(data.bot_steps)
    for bot_step in data["bot_steps"]:
        # print(key, data.bot_steps[key])
        db.bot_steps.insert_one(bot_step)
else:
    print("bot already present")