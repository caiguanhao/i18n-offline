from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os

def load_model(path):
    model = AutoModelForSeq2SeqLM.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained(path)
    return model, tokenizer

def load_models(directory):
    models = {}
    for d in os.listdir(directory):
        model = os.path.join(directory, d)
        if os.path.isdir(model):
            models[d] = load_model(model)
    return models

models = load_models('models')

app = Flask(__name__)

@app.route('/<model>', methods=['POST'])
def translate(model):
    if model not in models:
        return jsonify({ 'Message': 'Not supported' }), 400

    try:
        content = request.get_json(force=True).get('Content', '')
    except:
        content = ''
    if content == '':
        return jsonify({ 'Message': 'Content not provided' }), 400

    model, tokenizer = models[model]

    result = tokenizer.decode(model.generate(tokenizer.encode(content, return_tensors='pt')).squeeze(), skip_special_tokens=True)

    return jsonify({ 'Result': result })
