from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

print("Running MultiModal AI : \n")
print("*"*40)

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What is in this image? also create an caption for this image in about 50 words"
                },
                {
                    "type": "image_url",
                    "image_url": {"url":"https://jgu.edu.in/blog/wp-content/uploads/2024/01/shutterstock_434507533.jpg"},
                },
            ],
        },
    ],
)


print(response.choices[0].message.content)