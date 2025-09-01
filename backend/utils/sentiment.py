import requests
import os

HF_TOKEN = os.getenv("HF_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"

LABEL_MAP = {
    "LABEL_0": "NEGATIVE",
    "LABEL_1": "NEUTRAL",
    "LABEL_2": "POSITIVE"
}

def get_sentiment(text):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": text})

        if response.status_code != 200:
            print(f"[HuggingFace API Error] Status: {response.status_code}")
            print(f"Response Body: {response.text}")
            return "NEUTRAL", 0.0

        result = response.json()

        # Grab the top prediction
        top = result[0][0]
        label = LABEL_MAP.get(top['label'], "NEUTRAL")
        score = top['score']
        return label, score

    except Exception as e:
        print(f"[Sentiment Parsing Error] {e}")
        return "NEUTRAL", 0.0
