from flask import Flask
from flask import make_response, render_template, Response, jsonify, request
from app import app 

# Impedir que o usuário que deslogou do sistema volte a visualizar as páginas
def req(response:Response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

# Rota principal
@app.route('/')
def home():
    response = make_response(render_template('./homepage/index.html', title="Olá Mundo - CACAU"))
    return req(response)

@app.route("/get/data", methods=['GET','POST'])
def randomValues():

    index = None

    index = int(request.form['index'])

    if(index == 1):
        from random import randint
        data = [
            ("01-01-2020", randint(25,55), f'{randint(4,5)}.{randint(0,9)}', 15),
            ("02-01-2020", randint(25,55), f'{randint(4,5)}.{randint(0,9)}', 4),
            ("03-01-2020", randint(25,55), f'{randint(4,5)}.{randint(0,9)}', 5),
            ("04-01-2020", randint(25,55), f'{randint(4,5)}.{randint(0,9)}', 6),
            ("05-01-2020", randint(25,55), f'{randint(4,5)}.{randint(0,9)}', 4),
            ("06-01-2020", randint(25,55), f'{randint(4,5)}.{randint(0,9)}', 3)
        ]
        clone = "PS-1319"
    else:
        data = [
            ("01-01-2020", 28, 5.5, 15),
            ("02-01-2020", 40, 4.9, 4),
            ("03-01-2020", 50, 4.4, 4),
            ("04-01-2020", 55, 4.8, 4),
            ("05-01-2020", 55, 4.9, 4),
            ("06-01-2020", 50, 5.1, 4)
        ]
        clone = "PS-1319-TESTE"

    labels = [row[0] for row in data]
    temp = [row[1] for row in data]
    ph = [row[2] for row in data]
    brix = [row[3] for row in data]

    return jsonify(labels, temp, ph, brix, clone)


# Inicializador do sistema
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)