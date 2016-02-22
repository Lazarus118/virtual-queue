from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cors import CORS
#from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

# Setup SQLAlchemy for the project
db = SQLAlchemy(app)
CORS(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register application blueprints
from app.api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/api/v1')
