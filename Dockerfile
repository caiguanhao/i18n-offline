FROM python:3.12.4-bookworm

WORKDIR /app

ADD requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python3 -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-en-zh').save_pretrained('models/en-zh'); \
AutoModelForSeq2SeqLM.from_pretrained('Helsinki-NLP/opus-mt-en-zh').save_pretrained('models/en-zh');"

RUN python3 -c "from transformers import AutoTokenizer, AutoModelForSeq2SeqLM; \
AutoTokenizer.from_pretrained('Helsinki-NLP/opus-mt-zh-en').save_pretrained('models/zh-en'); \
AutoModelForSeq2SeqLM.from_pretrained('Helsinki-NLP/opus-mt-zh-en').save_pretrained('models/zh-en');"

ADD main.py .

CMD ["flask", "--debug", "--app", "main", "run", "--host=0.0.0.0", "--port=8181"]
