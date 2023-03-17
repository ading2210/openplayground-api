import openplayground
import sys

cookie = sys.argv[1]

client = openplayground.Client(cookie)
print(client.models)