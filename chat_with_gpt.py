import requests
import json
import random


with open('key_list.json', 'r', encoding='utf-8') as f:
    key_list = json.load(f)


base_url = 'openai.free-will.ai'


def chat_with_gpt(context, stream=False):
    # Round robin
    current_index = random.randint(0, len(key_list) - 1)
    API_KYE = key_list[current_index]['API_KEY']

    print('API KEY = ', API_KYE, flush=True)

    url = f'https://{base_url}/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer ' + API_KYE,
        'Content-Type': 'application/json'
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": context
    }

    if stream:
        data['stream'] = True
        response = requests.post(url, stream=True, headers=headers, json=data)
    else:
        response = requests.post(url, headers=headers, json=data)
        try:
            response = response.json()
        except BaseException as e:
            print('decode error:')
            print(e)
            print(response)

    return response

