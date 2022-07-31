from sanic import Sanic

from utils.config_manager import config

from api import api

app = Sanic(__name__)
app.blueprint(api)

app.run(host="0.0.0.0", port=config["api_service_port"],
        access_log=False)
