import argparse
import sys
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def download_model(name):
    model_name = f'Helsinki-NLP/opus-mt-{name}'
    model_path = f'models/{name}'
    sys.stderr.write(f"Downloading {model_name} to {model_path}...\n")
    AutoTokenizer.from_pretrained(model_name).save_pretrained(model_path)
    AutoModelForSeq2SeqLM.from_pretrained(model_name).save_pretrained(model_path)
    sys.stderr.write(f"Downloaded {model_name} to {model_path}\n")

def main():
    parser = argparse.ArgumentParser(description="Download translation models.")
    parser.add_argument('models', metavar='MODEL', type=str, nargs='+', help='model names to download (e.g., en-zh, zh-en)')
    args = parser.parse_args()
    for name in args.models:
        download_model(name)

if __name__ == "__main__":
    main()
