from flask import Flask
from flask import make_response, render_template, Response, jsonify, request
from app import app
from app.models.Fermentador import Fermentador
from app.models.Fermentador import Ciclo
from app.models.Fermentador import Historico

# Impedir que o usuário que deslogou do sistema volte a visualizar as páginas
def req(response:Response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

# Rota principal
@app.route('/')
def home():
    response = make_response(render_template('./homepage/index.html', title="Olá Mundo - CACAU"))
    return req(response)

@app.route('/get/all/fermentador', methods=['GET','POST'])
def listAllFermentador():
    all:Fermentador = Fermentador.query.all()
    return all

@app.route('/get/all/ciclo/fermentador/<id_machine>', methods=['GET','POST'])
def listAllCiclos(id_machine:int):
    result = []
    single:Fermentador = Fermentador.query.filter_by(id=id_machine).first()
    for ciclo in single.ciclos:
        ciclo:Ciclo = ciclo
        ciclo.generate()
        result.append(ciclo)
    return result

@app.route('/get/all/historico/ciclo/<id_ciclo>', methods=['GET','POST'])
def listAllHistorico(id_ciclo:int):
    result = []
    single:Ciclo = Ciclo.query.filter_by(id=id_ciclo).first()
    for historico in single.historicos:
        historico:Historico = historico
        result.append(historico)
    return result

# Inicializador do sistema
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)