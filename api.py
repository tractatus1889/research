"""OpenAI API calls."""

import datetime
import time
import wiki
from datetime import datetime
import openai
import os
# REPLACE THE FOLLOWING WITH YOUR OWN ORGANIZATION AND API KEY.
import auth
openai.organization = auth.ORGANIZATION
openai.api_key = auth.API_KEY


GPT4 = "gpt-4"
GPT3P5 = "gpt-3.5-turbo"
CURRENT_DATE = datetime.datetime.now()
FORMATTED_DATE = current_date.strftime("%B %d, %Y")
SYSTEM_INIT = f"You are a helpful assistant. Today's date is {FORMATTED_DATE}."
CONVERSATION = [
    {"role": "system", "content": SYSTEM_INIT},
]
MESSAGE_LOG = []

def get_response_continue(prompt):
  """Call GPT, continuing the current conversation."""
  new_message = {"role": "user", "content": prompt}
  CONVERSATION.append(new_message)
  MESSAGE_LOG.append(new_message)
  response = openai.ChatCompletion.create(
      model=GPT3P5,
      messages=CONVERSATION,
  )
  content = response["choices"][0]["message"]["content"]
  CONVERSATION.append({"role": "assistant", "content": content})
  MESSAGE_LOG.append({"role": "assistant", "content": content})
  return content


def get_response(prompt):
  """Call GPT from scratch, and do not continue the conversation."""
  new_message = {"role": "user", "content": prompt}
  messages = [{"role": "system", "content": SYSTEM_INIT},
              new_message]
  MESSAGE_LOG.append(new_message)
  errors = 0
  while True:
    if errors > 5:
      raise Exception("More than 5 RateLimitErrors.")

    try:
      response = openai.ChatCompletion.create(
          model=GPT3P5,
          messages=messages,
      )
      break
    except openai.error.RateLimitError:
      print("Hit RateLimitError.")
      time.sleep(2)
      errors += 1

  content = response["choices"][0]["message"]["content"]
  MESSAGE_LOG.append({"role": "assistant", "content": content})
  return content
