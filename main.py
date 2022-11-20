from flask import Flask
from flask import make_response, render_template, Response, jsonify, request
from app import app, db
from app.models.Fermentador import Fermentador
from app.models.Fermentador import Ciclo
from app.models.Fermentador import Historico
from datetime import datetime
from sqlalchemy import func, and_

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

@app.route('/get/all/historico/ciclo/<id_ciclo>/<timestamp>', methods=['GET','POST'])
@app.route('/get/all/historico/ciclo/<id_ciclo>', defaults={'timestamp': None}, methods=['GET','POST'])
def listAllHistorico(id_ciclo:int, timestamp:int):


    array_id = []
    array_ciclo = []
    array_ph = []
    array_brix = []
    array_temperatura = []
    array_datetime = []  
    result = []
    single:Ciclo = Ciclo.query.filter_by(id=id_ciclo).first()

    historicos = single.historicos

    if timestamp != None:
        timestamp = int(timestamp)
        date = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d')
        
        historicos = single.historicos.filter(and_(func.date(Historico.datetime) >= date, func.date(Historico.datetime) <= date)).all()

    for historico in historicos:
        historico:Historico = historico
        array_id.append(historico.id)
        array_ciclo.append(historico.id_ciclo)
        array_ph.append(historico.PH)
        array_brix.append(historico.brix)
        array_temperatura.append(historico.temperatura)
        array_datetime.append(datetime.timestamp(historico.datetime))  
    result.append(array_id)
    result.append(array_ph)
    result.append(array_ciclo)
    result.append(array_brix)
    result.append(array_temperatura)
    result.append(array_datetime)
    return result

@app.route('/get/date/range/ciclo/<id_ciclo>', methods=['GET','POST'])
def getRangeHistorico(id_ciclo:int  ):

    min = 0
    max = 0

    min = db.session.query(func.min(Historico.datetime)).filter(Historico.id_ciclo == id_ciclo).scalar()
    max = db.session.query(func.max(Historico.datetime)).filter(Historico.id_ciclo == id_ciclo).scalar()

    return jsonify({
        'min':f'{min.date()}',
        'max':f'{max.date()}'
    })

# Inicializador do sistema
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)