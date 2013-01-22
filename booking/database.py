from flask.ext.sqlalchemy import SQLAlchemy
from app import app
from settings import DB_PATH

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
db = SQLAlchemy(app)


