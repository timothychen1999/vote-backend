from flask import Flask,session,config
from Routes.user import user_routes
from Routes.metadata import metadata_routes
from Routes.login import login_routes
from Routes.utils import utils_routes
from Routes.items import items_routes
from Routes.coins import coins_routes
from flask_cors import CORS
import logging
import os

app = Flask(__name__)
app.register_blueprint(user_routes,url_prefix='/user')
app.register_blueprint(metadata_routes,url_prefix='/metadata')
app.register_blueprint(login_routes,url_prefix='/account')
app.register_blueprint(utils_routes,url_prefix='/utils')
app.register_blueprint(items_routes,url_prefix='/items')
app.register_blueprint(coins_routes,url_prefix='/coins')

@app.route('/')
def index():
    return 'Welcome to the Flask app!'


app.secret_key = os.getenv('SECRET_KEY')
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="None",
)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('Starting Flask app')
    logging.info(app.url_map)
    CORS(app)
    app.run(debug=True,host='0.0.0.0',port=8000)
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)