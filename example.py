import openplayground
import sys

cookie = sys.argv[1]

client = openplayground.Client(cookie)

prompt = "Summarize the GNU GPL v3."
for chunk in client.generate("openai:text-davinci-003", prompt):
  print (chunk)