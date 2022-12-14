from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from pathlib import Path

app = Flask(__name__, template_folder='./templates')
path = Path(__file__).parent.parent

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}/database.sqlite'

app.config['SECRET_KEY'] = 'MmM7NWFiYTlmYzdkYThxMDI1NJZiYTMiYjkzYTM0MDcwMGY4OGViNw=='

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Local padrão dos elementos estáticos
app.static_folder = 'static'