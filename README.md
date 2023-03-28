# Python OpenPlayground API
[![PyPi Version](https://img.shields.io/pypi/v/openplayground-api.svg)](https://pypi.org/project/openplayground-api/)

This is an unoffical API wrapper for the website [OpenPlayground](https://nat.dev), which provides access to a wide array of AI models for free, including ChatGPT, GPT-4, and Claude.

## Notice:
OpenPlayground has recently announced that they are going to starting deleting accounts that access their API via automated means (probably as as a direct response to this library). You should be fine as long as you don't send to many requests, since this library is able to bypass their bot detection by spoofing the `X-Session` header. They've also recently been requiring SMS verification upon signup, but this can easily be bypassed by signing in using a Google account. 

![screenshot from their discord server](https://media.discordapp.net/attachments/1072352756481929316/1088019955322196048/image.png)

## Features:
This library has the following abilities:
 - Log in using OTP code
 - List models
 - Generate text

## Installation:
You can install this library by running the following command:
```
pip3 install openplayground-api
```

## Documentation:
An example of how to use this library can be found in `/examples/example.py`.

### The `Model` Class:
The `openplayground.Model` class describes a model that is available to the user. Valid attributes are:
 - `provider` - The company that developed the model (e.g., openai, anthropic)
 - `name` - The name of the model, such as `text-davinci-003`.
 - `version` - The version of the model. This may return `None` on some models.
 - `tag` - A string that combines the provider and name, such as `openai:text-davinci-003`.
 - `params` - A dictionary containing possible parameters for the model.

### Authenticating With an OTP Code:
The `openplayground.Auth` class can be used to get your token using an OTP code emailed to you. Note that the following examples assume that `auth` is the name of your `openplayground.Auth` class.

```python
import openplayground
auth = openplayground.Auth()
```

#### Sending the OTP Code:
The `openplayground.Auth.send_otp_code` function sends an email containing the OTP code to the specificed email address. 

```python
auth.send_otp_code("sample@example.com")
```

#### Verifiying the OTP Code:
Once you have the OTP code, you can use the `openplayground.Auth.verify_otp_code` function to get your token from that OTP code. You can then use this token to create an `openplayground.Client` instance.

```python
otp_code = input("Enter OTP code: ")
token = auth.verify_otp_code()
```

### Using the Client:
The `openplayground.Client` class accepts two arguments, which is your account's email and its token. Your token can be obtained from the `__session` field in your browser's cookies, or using the `openplayground.Auth` class as shown above.

```python
import openplayground
client = openplayground.Client(email, token)
```

Note that the following examples assume `client` is the name of your `openplayground.Client` instance.

#### Downloading the Available Models:
The `client.get_models` function fetches the available models from `https://nat.dev/api/all_models`, and returns a dictionary of `openplayground.Model` objects. The client downloads the available models upon initialization and stores it in `client.models`, so calling this function shouldn't be necessary. 

Some popular model tags are:
 - OpenAI: `openai:gpt-4`, `openai:gpt-3.5-turbo`, `openai:text-davinci-003`
 - Anthropic: `anthropic:claude-instant-v1.0`, `anthropic:claude-v1.2`
 - Facebook/Stanford: `textgeneration:llama-65b`, `textgeneration:alpaca-7b`

```python
print(client.models.keys())
#dict_keys(['forefront:EleutherAI/GPT-J', 'forefront:EleutherAI/GPT-NeoX', 'forefront:pythia-12b', 'forefront:pythia-20b', 'forefront:pythia-6.9b', 'anthropic:claude-instant-v1.0', 'anthropic:claude-v1.2', 'textgeneration:alpaca-7b', 'textgeneration:llama-65b', 'huggingface:bigscience/bloomz', 'huggingface:google/flan-t5-xxl', 'huggingface:google/flan-ul2', 'cohere:command-medium-nightly', 'cohere:command-xlarge-nightly', 'cohere:medium', 'cohere:xlarge', 'openai:gpt-4', 'openai:code-cushman-001', 'openai:code-davinci-002', 'openai:gpt-3.5-turbo', 'openai:text-ada-001', 'openai:text-babbage-001', 'openai:text-curie-001', 'openai:text-davinci-002', 'openai:text-davinci-003'])
```

#### Generating Text:
The `client.generate` function generates some text given a model and a prompt. Optionally, you can also specify arguments such as the maximum length in the kwargs. You can find a list of valid arguments and their defaults in `openplayground.Model.params`. A few common ones are:
 - `maximum_length`
 - `temperature`
 - `top_k`
 - `top_p`

The values returned from this function are streamed and expressed in a dictionary. Note that GPT-4 access currently has a daily limit of around 10 requests/day, and may become paid in the future. 

Streamed example:
```python
for chunk in client.generate("openai:gpt-3.5-turbo", prompt):
  if chunk["event"] == "infer":
    print(chunk["message"], end="", flush=True)
```

Non-streamed example:
```python
message = ""
for chunk in client.generate("openai:gpt-3.5-turbo", prompt):
  if chunk["event"] == "infer":
    message += chunk["message"]
print(message)
```

### Misc:
#### Changing the Spoofed User-Agent:
You can change the global User-Agent by setting `openplayground.user_agent` right after importing the library.

```python
import openplayground
openplayground.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
```

## Copyright:
This project is licensed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt). Most of the code has been written by me, [ading2210](https://github.com/ading2210). A list of all the contributors can be found [here](https://github.com/ading2210/openplayground-api/graphs/contributors).