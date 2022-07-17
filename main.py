import datetime
import os
from pathlib import Path

import slack
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
max_amount_water = 2500
day_start = 8
day_end = 22


# removes all old messages
def remove_old_messages():
    messages = client.conversations_history(channel=os.environ['HYDRO_HOMIE_CHANNEL']).data['messages']
    for message in messages:
        client.chat_delete(channel=os.environ['HYDRO_HOMIE_CHANNEL'], ts=message['ts'])


# calculates the amount of water to be drunk between 8 am and 22 pm per hour
def calculate_amount_water():
    hours_between_start_and_end_of_day = day_end - day_start
    amount_water_per_hour = round(max_amount_water / hours_between_start_and_end_of_day)
    hours_since_start_of_day = datetime.datetime.now().hour - day_start
    amount_water_to_drink = amount_water_per_hour * hours_since_start_of_day
    return round(amount_water_to_drink / 1000, 2)


remove_old_messages()

message = client.chat_postMessage(channel=os.environ['HYDRO_HOMIE_CHANNEL'],
                                  text=f'Du solltest jetzt {calculate_amount_water()} Liter getrunken haben!')
