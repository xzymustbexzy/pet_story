from chat_with_gpt import chat_with_gpt


def write_story_by_captions(captions, pet_name, pet_type, consistent=True):
    captions = '\n'.join([f"图{i+1}: {caption}" for i, caption in enumerate(captions)])

    if consistent:
        prompt = f"""                 
            图片标题内容为: \n{captions}\n
            该标题中宠物的名字叫做{pet_name}。
            下面，请根据这些图的标题，发挥想象力，写一份{len(captions)}个段落的故事，段落的顺序需要与
            标题顺序严格对应对应，字数不超过150字。要求语义清晰、逻辑通顺，最好还能有一些文学性或深刻的寓
            意，段落之间需要有关联，最好能有承接。不要出现一些恐怖的、色情的、令人反感的、带有死亡事件的文
            字，同时避免不断重复类似的语句。请注意要用中文写故事！（宠物名字需要保持一致）。"""
    else:
        prompt = f"""                 
            图片标题内容为: \n{captions}\n
            该标题中宠物的名字叫做{pet_name}。
            下面，请根据这些图的标题，发挥想象力，写{len(captions)}个独立的小故事，段落的顺序需要与
            标题顺序严格对应对应，字数不超过150字。要求语义清晰、逻辑通顺，最好还能有一些文学性或深刻的寓
            意，内容本身可以简洁一些。请注意要用中文写故事！不要出现一些恐怖的、色情的、令人反感的、带有死亡事件的文
            字，同时避免不断重复类似的语句。（宠物名字需要保持一致）。"""

    prompt += """
        请遵循以下格式规范：
            [
                {
                    "title": "请复述一遍图片标题",
                    "content": "故事内容"
                },
            ]
        另外，请注意故事中对于宠物的第三人称应该称为“它”，对于主人或其他人类的第三人称应该称为“他”
    """

    messages=[
        {"role": "system", "content": f"You are a storyteller who specially tells some funny or warm stories to the pets drawn by users. Users will give you the captions of a series of pictures, and you need to develop rich imagination based on the titles and write a great stories."}, 
        {"role": "user", "content": prompt},
    ]

    response = chat_with_gpt(messages)
    try:
        r = response['choices'][0]['message']['content']
    except:
        print('OpenAI server error:')
        print(response)
        return response

    return r
