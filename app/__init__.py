from flask import Flask


app = Flask(__name__, template_folder='./templates')

# Local padrão dos elementos estáticos
app.static_folder = 'static'