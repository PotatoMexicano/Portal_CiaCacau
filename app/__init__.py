from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='./templates')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:/Desenvolvimento/Python_Projects/Companhia_do_Cacau/database.sqlite'

app.config['SECRET_KEY'] = 'MmM7NWFiYTlmYzdkYThxMDI1NJZiYTMiYjkzYTM0MDcwMGY4OGViNw=='

db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Local padrão dos elementos estáticos
app.static_folder = 'static'