# Python OpenPlayground API
[![PyPi Version](https://img.shields.io/pypi/v/openplayground-api.svg)](https://pypi.org/project/openplayground-api/)

This is an unoffical API wrapper for the website [OpenPlayground](https://nat.dev), which provides access to a wide array of AI models for free.

## Features:
This library has the following abilities:
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
 - `tag` - A string that combines the provider and name in this format: `<provider>:<name>`. Example: `openai:text-davinci-003`
 - `params` - A dictionary containing possible parameters for the model.

### Logging In With an Email:
The `openplayground.Auth` class can be used to get your token using an OTP code emailed to you. 

The `openplayground.Auth.login_part_1` function sends an email containing the OTP code to the specificed email address. Once you have the OTP code, you can use the `openplayground.Auth.login_part_2` function to get your token from that OPT code.

### Initializing the Client:
The `openplayground.Client` class accepts one argument, which is your account's token. Your token can be obtained from the `__session` field in your browser's cookies, or using the `openplayground.Auth` class as show above.

### Downloading the Available Models:
The `openplayground.Client.get_models` function fetches the available models from `https://nat.dev/api/all_models`, and returns a dictionary of `openplayground.Model` objects.

### Generating Text:
The `openplayground.Client.generate` function generates some text given a model and a prompt. Optionally, you can also specify arguments such as the maximum length in the kwargs. You can find a list of valid arguments and their defaults in `openplayground.Model.params`. A few common ones are:
 - `maximum_length`
 - `temperature`
 - `top_k`
 - `top_p`

The values returned from this function are streamed and expressed in a dictionary.

## Copyright:
This project is licensed under the [GNU GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt). Most of the code has been written by me, [ading2210](https://github.com/ading2210). A list of all the contributors can be found [here](https://github.com/ading2210/openplayground-api/graphs/contributors).