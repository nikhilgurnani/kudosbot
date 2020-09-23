from functools import lru_cache
from fastapi import FastAPI, Request, Response
from slack import WebClient
import json
from typing import Any, Dict
import random
import re

import config


app = FastAPI()

@lru_cache()
def get_settings():
    return config.Settings()

def get_slack_client():
    return WebClient(token=get_settings().slack_auth_token)

@app.post("/direct")
async def post_kudos(request: Request):
    try:

        body = await request.form()
        data = json.loads(body['payload'])

        values = data['view']['state']['values']
        channel_id = values['channel']['id']['selected_channel']
        message = values['custom']['message']['value']
        users = [ "<@" + user + ">" for user in values['receivers']['id']["selected_users"] ]
        sender = data['user']

        client = get_slack_client()

        try:
            response = client.conversations_join(channel=channel_id)
        except Exception as e:
            print(str(e))

        payload = "\n\n Hi " + " ".join(users) + " :wave:\nYou've just been kudo-ed by <@" + sender['id'] + "> :clap:\
            \n\"_" + message + "_\" :cherry_blossom:\nSay thank you now! :cake:"

        client.chat_postMessage(text=payload, channel=channel_id)


        return Response(status_code=200)

    except Exception as e:
        print(str(e))
        return {
            "response_type": "ephemeral",
            "text": "💩 Poopknuckels! Something just went haywire. Please try again!"
        }

@app.post("/modal")
async def post_modal(request: Request):
    try:
        body = await request.form()
        with open('./modal/kudos.json') as f:
            data = json.load(f)
        client = get_slack_client()
        client.views_open(trigger_id=body['trigger_id'], view=data)

        responses = [
                "Fantastic! You just made someone's day better :dog: ",
                "They get a kudos! You get a kudos! EVERYBODY :clap: GETS :clap: KUDOS :clap:",
                "Good shit! Keep that shit up, yo :sunglasses:",
                "Tu toh dev manus nikla re!"
        ];

        return {
            "response_type": "ephemeral",
            "text": responses[random.randint(0,3)]
        }
    except Exception as e:
        print(str(e))
        return {
            "response_type": "ephemeral",
            "text": "💩 Poopknuckels! Something just went haywire. Please try again!"
        }