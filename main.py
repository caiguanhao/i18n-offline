from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TextIteratorStreamer
import os
from threading import Thread
import asyncio
import websockets
import argparse

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

async def handler(websocket, path):
    async for content in websocket:
        model = path.lstrip('/')
        if model not in models:
            return await websocket.send('Not supported')
        model, tokenizer = models[model]
        paragraphs = content.split('\n')
        for i, paragraph in enumerate(paragraphs):
            if i > 0: await websocket.send('\n')
            if not paragraph.strip(): continue
            input_ids = tokenizer(paragraph, return_tensors='pt', truncation=True).input_ids
            streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)
            thread = Thread(target=model.generate, kwargs=dict(
                input_ids=input_ids,
                streamer=streamer,
                num_beams=1,
            ))
            thread.start()
            for text in streamer:
                if text == '': continue
                if text[-4:] == "</s>": text = text[:-4]
                await websocket.send(text)
        return

async def main(addr, port):
    server = await websockets.serve(handler, addr, port)
    print(f"WebSocket server is running on {addr}:{port}")
    await server.wait_closed()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='WebSocket Server')
    parser.add_argument('--addr', type=str, default='127.0.0.1', help='Address to bind the server, defaults to 127.0.0.1')
    parser.add_argument('--port', type=int, default=8765, help='Port to bind the server, defaults to 8765')
    args = parser.parse_args()
    asyncio.run(main(args.addr, args.port))
