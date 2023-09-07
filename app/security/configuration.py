from app.web.configuration import flask_app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(flask_app)
