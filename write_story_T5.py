# Importing libraries
import os
import json
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
import os
from tqdm.notebook import tqdm

# Importing the T5 modules from huggingface/transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration


device = 'cuda' if torch.cuda.is_available() else 'cpu'
model_name = 'nikoyo/pet-mt5-base'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
model = model.to(device)


class YourDataSetClass(Dataset):
    """
    Creating a custom dataset for reading the dataset and 
    loading it into the dataloader to pass it to the neural network for finetuning the model

    """

    def __init__(self, data, tokenizer, source_len):
        self.tokenizer = tokenizer
        self.data = data
        self.source_len = source_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        source_text = self.data[index]['input']

        #cleaning data so as to ensure data is in string type
        source_text = ' '.join(source_text.split())

        source = self.tokenizer.batch_encode_plus(
                [source_text], 
                max_length=self.source_len, 
                pad_to_max_length=True, 
                truncation=True, 
                padding="max_length", 
                return_tensors='pt')

        source_ids = source['input_ids'].squeeze()
        source_mask = source['attention_mask'].squeeze()

        return {
            'source_ids': source_ids.to(dtype=torch.long), 
            'source_mask': source_mask.to(dtype=torch.long), 
        }
    

def validate(tokenizer, model, device, loader):
    """
    Function to evaluate model for predictions
    """
    model.eval()
    predictions = []
    with torch.no_grad():
        for _, data in enumerate(loader, 0):
            ids = data['source_ids'].to(device, dtype = torch.long)
            mask = data['source_mask'].to(device, dtype = torch.long)

            generated_ids = model.generate(
                input_ids = ids,
                attention_mask = mask, 
                max_length=200, 
                num_beams=10,
                repetition_penalty=2.5,
                length_penalty=1.0, 
                early_stopping=True,
                use_cache=True,
                do_sample=True,
                temperature=0.8,
                top_k=50,
                top_p=0.95
            )
            preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]

            predictions.extend(preds)
    return predictions


def inference(captions, pet_name, pet_type):
    global tokenizer, model

    data = []
    for caption in captions:
        data.append({
            'input': f'根据描述写一个关于{pet_type} “{pet_name}”的故事：{caption}'
        })
    data_set = YourDataSetClass(data, tokenizer, 300)
    loader = DataLoader(data_set, batch_size=1, shuffle=False, num_workers=1)
    predictions = validate(tokenizer, model, device, loader)
    return '\n'.join(predictions)
