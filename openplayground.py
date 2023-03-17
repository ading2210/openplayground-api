import requests

class Model:
  def __init__(self, data):
    self.provider = data.get("provider")
    self.name = data.get("name")
    self.version = data.get("version")
    self.params = data.get("parameters")

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

    models = []
    for key in data:
      model = Model(data[key])
      models.append(model)

    return models