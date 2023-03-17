import requests, json, re

class Model:
  def __init__(self, data):
    self.provider = data.get("provider")
    self.name = data.get("name")
    self.version = data.get("version")
    self.params = data.get("parameters")
    self.tag = f"{self.provider}:{self.name}"
  
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