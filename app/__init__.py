from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='./templates')


app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///E:/Desenvolvimento/CiaCacau/database.sqlite'

app.config['SECRET_KEY'] = 'MmM7NWFiYTlmYzdkYThxMDI1NJZiYTMiYjkzYTM0MDcwMGY4OGViNw=='

db = SQLAlchemy(app)

# Local padrão dos elementos estáticos
app.static_folder = 'static'