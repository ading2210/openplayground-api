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

email = args.email or ""
if args.token:
  token = args.token
else:
  auth = openplayground.Auth()
  auth.send_otp_code(args.email)
  otp_code = input("enter otp key: ")
  token = auth.verify_otp_code(otp_code)
  print("Your token: " + token)

client = openplayground.Client(token, email=email)
prompt = "Summarize the GNU GPL v3."

for chunk in client.generate("openai:gpt-3.5-turbo", prompt, maximum_length=1000):
  if chunk["event"] == "infer":
    print(chunk["message"], end="", flush=True)