"""Chat interface."""

import api
from datetime import datetime


def chat_interface():
    print("Welcome to the Chat Interface!")
    while True:
        prompt = input("Your input ('exit' to exit): ")
        if prompt.lower() == 'exit':
            break
        content_json = api.get_response_continue(prompt)
        print("Response:", content_json["content"])


chat_interface()
