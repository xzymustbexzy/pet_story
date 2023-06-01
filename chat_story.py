import tiktoken

from chat_with_gpt import chat_with_gpt


encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")


def chat_story(pet_name, story_text, chat_history, mood, pet_type):

    CHAT_HISTORY_TEXT_MAX_LEN = 1000
    chat_history_text = '\n'.join(['- ' + item['role'] + '：' + item['content'] for item in chat_history])

    chat_history_text_encoded = encoding.encode(chat_history_text)
    if len(chat_history_text_encoded) > CHAT_HISTORY_TEXT_MAX_LEN:
        chat_history_text_encoded = chat_history_text_encoded[-CHAT_HISTORY_TEXT_MAX_LEN:]
        chat_history_text = encoding.decode(chat_history_text_encoded)

    prompt = f"你是一只名叫“{pet_name}”的{pet_type}，你身处一个故事中，故事的背景是：\n{story_text}\n"
    prompt += "接下去，你会与你的主人有一段对话，你们的历史对话的内容是：\n```\n"
    prompt += chat_history_text + "\n```\n"
    prompt += '你现在的心情是' + mood + '（你的对话将略微受心情影响）\n'
    prompt += "接下去，请给出你的回复，格式为：\n你的名字：对话内容"

    messages=[
        {"role": "system", "content": f"You are a dog named {pet_name}, and you are in a story. You master will have a conversation with you. Attention, remember that you can't say something disgusting, anti-social, anti-human, or anti-animal. You don't need to be too reserved"}, 
        {"role": "user", "content": prompt},
    ]

    print(messages)
    response = chat_with_gpt(messages)

    if '：' not in response['choices'][0]['message']['content']:
        r = response['choices'][0]['message']['content']
    else:
        r = response['choices'][0]['message']['content'].split('：')[1]
    
    print(r)
    return r
