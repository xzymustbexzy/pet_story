import requests


data = {
    'captions': ['a dog is wearing a harness and looking at the camera'],
    'pet_name': 'haha',
    'pet_type': 'man',
    'consistent': False,
    'model': 'T5'
}

r = requests.post('http://localhost:5888/write_story', json=data)
print(r.json())
