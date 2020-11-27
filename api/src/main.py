#!/usr/bin/env python

import os
import logging

from flask import Flask, jsonify, redirect
from flask_cors import CORS

from routes import errors
from routes import MAIN_PREFIX, API_PREFIX
from routes.requests import Blueprint as RequestBlueprint
from settings import ZIMFARM_API_URL
from utils import ZimitEncoder
from zimfarm import test_connection

application = Flask(__name__)
application.json_encoder = ZimitEncoder
CORS(application)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s: %(levelname)s] %(message)s"))
logger.addHandler(handler)


@application.route(f"{MAIN_PREFIX}/")
def noversion():
    return redirect(f"{API_PREFIX}")


@application.route(f"{API_PREFIX}")
def home():
    return jsonify({"success": True})


@application.route(f"{API_PREFIX}/test")
def test():
    return jsonify({"zimfarm_api": ZIMFARM_API_URL, "connected": test_connection()})


application.register_blueprint(RequestBlueprint())
errors.register_handlers(application)

if __name__ == "__main__":
    # Initializer.create_initial_user()
    application.run(
        host=os.getenv("BINDING_HOST", "localhost"),
        debug=os.getenv("DEBUG", True),
        port=int(os.getenv("BINDING_PORT", 8000)),
        threaded=True,
    )
