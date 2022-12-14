from flask import Flask
from flask import make_response, render_template, Response, jsonify, request, session, flash, redirect, url_for
from app import app, db
from app.models.Fermentador import Fermentador
from app.models.Fermentador import Ciclo
from app.models.Fermentador import Historico
from app.models.Fermentador import Usuario
from datetime import datetime, timedelta
from sqlalchemy import func, and_, cast, Date
from flask_login import login_user, login_required, current_user

# Impedir que o usuário que deslogou do sistema volte a visualizar as páginas
def req(response:Response):
    response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    return response

@app.errorhandler(401)
def error_401(_): 
    flash("Acesso negado", category='warning')
    return redirect(url_for('login'))

# Rota principal
@app.route('/')
@login_required
def home():
    response = make_response(render_template('./homepage/index.html', title="Homepage - CACAU"))
    return req(response)

@app.route('/get/all/fermentador', methods=['GET','POST'])
@login_required
def listAllFermentador():
    all:Fermentador = Fermentador.query.all()
    return all

@app.route('/get/all/ciclo/fermentador/<id_machine>', methods=['GET','POST'])
@login_required
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
@login_required
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
        # date = datetime.fromtimestamp(timestamp / 1000) #forSQLServer


        # date_in =  date + timedelta(hours=0, minutes=0, seconds=0) #forSQLServer
        # date_out = date +timedelta(hours=23, minutes=59, seconds=59) #forSQLServer

        historicos = single.historicos.filter(and_(func.date(Historico.datetime) >= date, func.date(Historico.datetime) <= date)).all()
        # historicos = single.historicos.filter(cast(Historico.datetime, Date) >= date_in).filter(cast(Historico.datetime, Date) <= date_out).all() #forSQLServer
    
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
@login_required
def getRangeHistorico(id_ciclo:int):

    min = 0
    max = 0

    min = db.session.query(func.min(Historico.datetime)).filter(Historico.id_ciclo == id_ciclo).scalar()
    max = db.session.query(func.max(Historico.datetime)).filter(Historico.id_ciclo == id_ciclo).scalar()

    return jsonify({
        'min':f'{min.date()}',
        'max':f'{max.date()}'
    })

@app.route('/auth/logout', methods=['GET','POST'])
def auth_logout():
    
    logout_user();
    session.clear();

    return app.login_manager.unauthorized()

@app.route('/auth/login', methods=['GET','POST'])
def auth_login():

    login = str(request.form['username'])
    pwd = str(request.form['password'])

    usuario:Usuario = Usuario.query.filter_by(login=login).first()

    resultado = None

    if (usuario):
        resultado = usuario.verify_password(pwd)
        
        if resultado:
            session.clear()
            login_user(usuario)

            return jsonify({
                'status':200,
                'message':'Usuário autenticado'
                }), 200

        else:
            return jsonify({
                'status': 403,
                'message':'Senha incorreta'
                }), 200

    else:
        return jsonify({
            'status':404,
            'message':'Usuário não encontrado'
            }), 200
    
@app.route('/login')
def login():

    if(current_user.is_authenticated): return redirect(url_for('home'))

    response = make_response(render_template('./login/index.html', title="Login - CACAU"))
    return req(response)


# Inicializador do sistema
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)