import openplayground
import dotenv
import os
import sys

token_name = "OPENPLAYGROUND_TOKEN"
email_name = "OPENPLAYGROUND_EMAIL"

prompt = "Summarize the GNU GPL v3."
for chunk in client.generate("openai:text-davinci-003", prompt, maximum_length=1000):
  if chunk["event"] == "infer":
    print(chunk["message"], end="", flush=True)