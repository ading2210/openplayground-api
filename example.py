import openplayground
import sys

token = sys.argv[1]
client = openplayground.Client(token)

prompt = "Summarize the GNU GPL v3."
for chunk in client.generate("openai:text-davinci-003", prompt, maximum_length=1000):
  if chunk["event"] == "infer":
    print(chunk["message"], end="", flush=True)