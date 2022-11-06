from flask import Flask
from flask import make_response, render_template, Response, jsonify
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

    result = []

    from random import randint
    data = [
        ("01-01-2020", randint(25, 40), randint(4, 8)),
        ("01-02-2020", randint(25, 40), randint(4, 8)),
        ("01-03-2020", randint(25, 40), randint(4, 8)),
        ("01-04-2020", randint(25, 40), randint(4, 8)),
        ("01-05-2020", randint(25, 40), randint(4, 8)),
        ("01-06-2020", randint(25, 40), randint(4, 8)),
        ("01-07-2020", randint(25, 40), randint(4, 8)),
        ("01-08-2020", randint(25, 40), randint(4, 8)),
        ("01-09-2020", randint(25, 40), randint(4, 8)),
        ("01-10-2020", randint(25, 40), randint(4, 8)),
        ("01-11-2020", randint(25, 40), randint(4, 8)),
        ("01-12-2020", randint(25, 40), randint(4, 8)),
    ]

    labels = [row[0] for row in data]
    temp = [row[1] for row in data]
    ph = [row[2] for row in data]

    # for item in data:
    #     temp = {}
    #     temp['label'] = item[0]
    #     temp['temp'] = item[1]
    #     temp['ph'] = item[2]
    #     result.append(temp)

    return jsonify(labels, temp, ph)


# Inicializador do sistema
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)