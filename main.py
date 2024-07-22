from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, TextIteratorStreamer
import os
from threading import Thread
import asyncio
import websockets

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
        input_ids = tokenizer(content, return_tensors='pt').input_ids
        streamer = TextIteratorStreamer(tokenizer, skip_prompt=True)
        thread = Thread(target=model.generate, kwargs=dict(
            input_ids=input_ids,
            streamer=streamer,
            num_beams=1,
        ))
        thread.start()
        for text in streamer:
            if text == '': continue
            await websocket.send(text)
        await websocket.close()

async def main():
    server = await websockets.serve(handler, 'localhost', 8765)
    print("WebSocket server is running on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
