import openplayground
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--email', type=str)
parser.add_argument('--token', type=str)
args = parser.parse_args()

if len(sys.argv) <= 1:
  print("This program requires arguments!")
  sys.exit(1)

if args.email:
  auth = openplayground.Auth()
  auth.send_otp_code(args.email)
  otp_code = input("enter otp key: ")
  token = auth.verify_otp_code(otp_code)
if args.token:
  token = args.token

client = openplayground.Client(token)
prompt = "Summarize the GNU GPL v3."
for chunk in client.generate("openai:gpt-4", prompt, maximum_length=1000):
  if chunk["event"] == "infer":
    print(chunk["message"], end="", flush=True)