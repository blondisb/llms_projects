# from langchain_groq import ChatGroq

import os
import base64
from groq import Groq
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)
client = Groq(api_key = os.environ.get("GROQ_API_KEY"))



def basic_test() -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


def llava_model_usage() -> str:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            # "url": "https://example.com/image.png",
                            "url": "https://upload.wikimedia.org/wikipedia/commons/f/f6/AK-47_assault_rifle.jpg",
                        },
                    },
                ],
            }
        ],
        model="llava-v1.5-7b-4096-preview",
    )
    return chat_completion.choices[0].message.content


def encode_picture(pic_path: str) -> str:
    with open(pic_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string.decode('utf-8')

def llava_using_my_pictures(pic_path: str, question: str) -> str:
    b64_picture = encode_picture(pic_path)
    
    try:
        chat_completion = client.chat.completions.create(
            messages = [
                # {
                #     "role": "system",
                #     "content": "you're medical expert x-ray cheking. You will give me answers with names and exact body parts.",
                # },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_picture}"},
                        },
                    ],
                }
            ],
            model="llava-v1.5-7b-4096-preview",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return e

if __name__ == '__main__':
    print(1)
    # print(basic_test())
    # print(llava_model_usage())
    
    # pic_path = "./media/afrika_twin.jpg"
    # pic_path = "./media/ejercicio_limites1.jpg"
    # pic_path = "./media/radiografia.jpg"
    pic_path = "./media/my_finger.jpg"

    # question = "Writhe in LATEX the following equation"
    # question = "rewrite the following equation "
    # question = "what do you see?"
    # question = "extract the text from the following picture"

    # question = "you see something wrong with this patient?"
    # question = "This is the x-ray of a patient. What problems do you detect?"
    question = "This is a finger x-ray. What problems do you detect? Can you observe a medical conditions on that?"

    print(llava_using_my_pictures(pic_path, question))