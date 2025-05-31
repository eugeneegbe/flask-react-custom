import dotenv
import os
import json


class ENVIRONMENT:
    def __init__(self):
        dotenv.load_dotenv(os.path.dirname(__file__) + '/.venv')

        self.port = os.getenv("PORT")
        self.prefix = os.getenv("PREFIX")
        self.domain = os.getenv("DOMAIN")

    def get_instance(self):
        if not hasattr(self, "_instance"):
            self._instance = ENVIRONMENT()
        return self._instance

    def getDomain(self):
        return self.domain

    def getPort(self):
        return self.port

    def getPrefix(self):
        return self.prefix


domain = ENVIRONMENT().get_instance().getDomain()
port = ENVIRONMENT().get_instance().getPort()
prefix = ENVIRONMENT().get_instance().getPrefix()


def build_swagger_config_json():
    config_file_path = os.path.dirname(__file__) +  '/swagger/config.json'

    with open(config_file_path, 'r') as file:
        config_data = json.load(file)

    config_data['servers'] = [
        {"url": f"http://localhost:{port}{prefix}"},
        {"url": f"http://{domain}:{port}{prefix}"}
    ]

    new_config_file_path = os.path.dirname(__file__) +  '/swagger/config.json'

    with open(new_config_file_path, 'w') as new_file:
        json.dump(config_data, new_file, indent=2)
