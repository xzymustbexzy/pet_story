import requests

url = 'http://localhost:5888/chat_story'

chat_history = [
    {
        'role': '主人',
        'content': '你好，中分'
    }
]

pet_name = '中分'
story_text = '中分是一只非常喜欢在花丛中玩耍的猫。今天，它跑到一片花海里，被五颜六色的花儿迷住了眼。蹭蹭花瓣，扭动腰肢，中分好不开心。它觉得自己仿佛成了花海里最闪耀的那一朵。'

r = requests.post(url, json={
    'chat_history': chat_history,
    'pet_name': pet_name,
    'story_text': story_text
})

print(r.json())

