import openplayground
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--email', type=str)
parser.add_argument('--token', type=str)
args = parser.parse_args()

auth = openplayground.Auth()

if len(sys.argv) > 1:
  if args.email:
    auth.login_part_1(args.email)
    print("token: " + auth.login_part_2(input("enter otp key :")))
    exit()
    
  if args.token:
    client = openplayground.Client(args.token)
    prompt = "Summarize the GNU GPL v3."
    for chunk in client.generate("openai:gpt-4", prompt, maximum_length=1000):
      if chunk["event"] == "infer":
        print(chunk["message"], end="", flush=True)

