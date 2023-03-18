import openplayground
import dotenv
import os
import sys

token_name = "OPENPLAYGROUND_TOKEN"
email_name = "OPENPLAYGROUND_EMAIL"

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

auth = openplayground.Auth()

if len(sys.argv) > 1:
  token = sys.argv[1]
  client = openplayground.Client(token)

else:
  if os.environ.get(email_name) is None:
    print("create .env environment and set OPENPLAYGROUND_EMAIL to your email.")
    exit()
  
  else:
    email=os.environ[email_name]
    print("using email :", email) 
    
    if os.environ.get(token_name) is None:
      print("there is no token, preparing to authenticate...")
      auth.login_part_1(email)
      auth.login_part_2()
      os.environ[token_name] = auth.login_part_3(input("enter otp key :"))
      dotenv.set_key(dotenv_file, token_name, os.environ[token_name])

    token=os.environ[token_name]
    print("using token :", token) 
    client = openplayground.Client(token)



prompt = "Summarize the GNU GPL v3."
for chunk in client.generate("openai:gpt-4", prompt, maximum_length=1000):
  if chunk["event"] == "infer":
    print(chunk["message"], end="", flush=True)