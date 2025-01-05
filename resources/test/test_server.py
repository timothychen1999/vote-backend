from flask import Flask,session,config
from test.Routes.test_ia import ia_routes
from test.Routes.test_va import va_routes

from flask_cors import CORS
import logging
import os

app = Flask(__name__)
app.register_blueprint(va_routes,url_prefix='/VA')
app.register_blueprint(ia_routes,url_prefix='/IA')


@app.route('/')
def index():
    return 'Welcome to the Flask app!'

@app.route('/get_candidates')
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