import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


def ask_llm(messages, temperature=0.3):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=temperature,
        messages=messages
    )

    return response.choices[0].message.content