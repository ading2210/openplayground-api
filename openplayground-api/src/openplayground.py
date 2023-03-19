import requests, json, re

class Model:
  def __init__(self, data):
    self.provider = data.get("provider")
    self.name = data.get("name")
    self.version = data.get("version")
    self.params = data.get("parameters")
    self.tag = f"{self.provider.strip()}:{self.name.strip()}"
  
  def resolve_params(self, kwargs):
    final_params = {}
    for param_name in self.params:
      if param_name in kwargs:
        final_params[param_name] = kwargs[param_name]
      else:
        final_params[param_name] = self.params[param_name]["value"]

    return final_params

class Client:
  api_url = "https://nat.dev/api"

  def __init__(self, token):
    self.session = requests.Session()
    self.headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
      "Referrer": "https://nat.dev/",
      "Host": "nat.dev",
      "Authorization": f"Bearer {token}"
    }
    self.session.headers.update(self.headers)

    self.models = self.get_models()
  
  def get_models(self):
    models_url = self.api_url + "/all_models"
    r = self.session.get(models_url)
    data = r.json()

    models = {}
    for key in data:
      model = Model(data[key])
      models[key] = model

    return models
  
  def generate(self, model, prompt, **kwargs):
    if not isinstance(model, Model):
      model = self.models[model]

    generation_url = self.api_url + "/stream"
    payload = {
      "models": [
        {
          "name": model.tag,
          "parameters": model.resolve_params(kwargs),
          "provider": model.provider,
          "tag": model.tag,
        }
      ],
      "prompt": prompt
    }
    r = self.session.post(generation_url, json=payload, stream=True)

    for chunk in r.iter_content(chunk_size=None):
      r.raise_for_status()
      
      chunk_str = chunk.decode()
      data_regex = r"event:(\S+)\sdata:(.+)\s"
      matches = re.findall(data_regex, chunk_str)[0]

      data = json.loads(matches[1])
      data["event"] = matches[0]
      yield data

class Auth:
  api_url = "https://clerk.nat.dev/v1/client/sign_ins/"

  def __init__(self):
    self.session = requests.Session()
    self.headers = {
      "Host": "clerk.nat.dev",
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
      "Origin": "https://accounts.nat.dev"
    }
    self.session.params = {
      "_clerk_js_version": "4.32.5"
    }

    self.session.headers.update(self.headers)
  
  #send verification email
  def login_part_1(self, email_address):
    self.data= {
      "identifier": email_address,
    }

    res = self.session.post(self.api_url, self.data)
    self.session.cookies = res.cookies
    self.api_url_sia = res.json()["response"]["id"]
    self.email_id = res.json()["client"]["sign_in_attempt"]["supported_first_factors"][0]["email_address_id"]

    self.data = {
      "email_address_id": self.email_id,
      "strategy": "email_code"
    }
    self.session.post(self.api_url + self.api_url_sia + '/prepare_first_factor', self.data)
  
  #otp process
  def login_part_2(self, code):
    self.data = {
      "strategy": "email_code",
      "code": code,
    }
    res = self.session.post(self.api_url + self.api_url_sia + '/attempt_first_factor', self.data)
    token = res.json()["client"]["sessions"][0]["last_active_token"]["jwt"]
    return token


