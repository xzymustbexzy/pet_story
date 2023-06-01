import os

import flask
from flask_cors import CORS

from write_story import write_story_by_captions
from write_story_T5 import inference as T5_story_model_inference
from chat_story import chat_story


app = flask.Flask(__name__)
CORS(app)


@app.route('/ping', methods=['GET'])
def ping():
    return 'pong'


@app.route('/write_story', methods=['POST'])
def write_story_entry():
    data = flask.request.json
    captions = data['captions']
    pet_name = data['pet_name']
    pet_type = data['pet_type']
    consistent = data['consistent']
    model = 'GPT'
    if 'model' in data:
        model = data['model']
    
    if model == 'GPT':
        story = write_story_by_captions(captions, pet_name, pet_type, consistent)
    elif model == 'T5':
        story = T5_story_model_inference(captions, pet_name, pet_type)
    else:
        return {
            'code': 1,
            'story': f'Model {model} not found'
        }
    return {
        'code': 0,
        'story': story,
    }


@app.route('/chat_story', methods=['POST'])
def chat_story_entry():
    data = flask.request.json
    chat_history = data['chat_history']
    pet_name = data['pet_name']
    story_text = data['story_text']
    pet_type = data['pet_type']
    mood = data['mood']
    story = chat_story(pet_name, story_text, chat_history, mood, pet_type)
    return {
        'code': 0,
        'story': story,
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5888, threaded=True)


