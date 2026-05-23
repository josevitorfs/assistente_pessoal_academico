import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GEMMA_API_KEY")

client = OpenAI(
    base_url="https://llm.liaufms.org/v1/gemma-3-12b-it",
    api_key=api_key
)


def ask_gemma(prompt):

    try:

        response = client.chat.completions.create(

            model="google/gemma-3-12b-it",

            temperature=0.3,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"Erro ao acessar LLM: {str(e)}"