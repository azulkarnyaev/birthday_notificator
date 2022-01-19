import json
from functools import lru_cache
from typing import List

import boto3 as boto3
import requests
from boto3.dynamodb.conditions import Key

from birthday_notificator import birthday_reader
from birthday_notificator.date_extractor import extract_date_key
from birthday_notificator.notification_builder import build_congratulation
from birthday_notificator.personal_info import Relation, Language
from birthday_notificator.random_notification_picker import pick_random_notification


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TelegramCongratulation')

    current_date_key = extract_date_key(event)

    scan_kwargs = {
        'FilterExpression': Key('birthday').eq(current_date_key)
    }
    done = False
    start_key = None

    print(f"Lambda got event={event}, date_key={current_date_key}")

    ssm = boto3.client('ssm')
    telegram_bot_ssm_key = ssm.get_parameter(Name='/notification_service/encrypted_telegram_key', WithDecryption=True)
    telegram_bot_key = telegram_bot_ssm_key['Parameter']['Value']

    @lru_cache(maxsize=1000)
    def read_congratulations(relation: Relation, language: Language) -> List[str]:
        congratulation_table = dynamodb.Table('Congratulation')
        congrats = congratulation_table.query(
            KeyConditionExpression=Key('type').eq(language.name + "#" + relation.name)
        )
        items = congrats.get('Items', [])
        return [i['text'] for i in items]

    while not done:
        if start_key:
            scan_kwargs['ExclusiveStartKey'] = start_key
        response = table.scan(**scan_kwargs)

        birthdays = birthday_reader.read_birthdays(lambda: response.get("Items", []))
        for birthday in birthdays:
            congrats_text = build_congratulation(birthday, pick_random_notification, read_congratulations)
            body = {
                "text": congrats_text,
                "parse_mode": "MarkdownV2",
                "chat_id": birthday.target_chat_id
            }
            tg_response = requests.post(
                f"https://api.telegram.org/bot{telegram_bot_key}/sendMessage",
                json=body)
            print(f"Telegram API response code: {tg_response.status_code}")

        print(f'birthdays: {birthdays}')
        start_key = response.get('LastEvaluatedKey', None)
        done = start_key is None
    return {
        'statusCode': 200,
        'body': json.dumps(f'Received event: {event}')
    }
