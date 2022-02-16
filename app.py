from flask import Flask
from flask import request
from flask import Response
import json
import config_api
app = Flask(__name__)

config_api.configure(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)