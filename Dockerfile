FROM python:3.12.4-slim-bookworm

WORKDIR /app

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD download.py .

RUN python3 download.py en-zh zh-en && rm -rf /root/.cache/huggingface

ADD main.py .

CMD ["python3", "main.py", "--addr=0.0.0.0", "--port=8765"]
