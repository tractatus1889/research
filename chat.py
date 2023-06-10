"""Chat interface."""

import api
from datetime import datetime


def chat_interface():
    print("Welcome to the Chat Interface!")
    while True:
        prompt = input("Your input ('exit' to exit): ")
        if prompt.lower() == 'exit':
            break
        content = api.get_response_continue(prompt)
        print("Response:", content)


def write_conversation():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")
    filename = f"conversations/{formatted_datetime}.txt"
    with open(filename, "w") as f:
        for message in api.CONVERSATION:
            f.write(f"{message['role']}: {message['content']}\n")


chat_interface()
write_conversation()
