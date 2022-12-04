
from dataclasses import dataclass
from datetime import datetime, date, time

from app import db

@dataclass
class Fermentador(db.Model):
    __tablename__ = 'fermentador'

    id:int
    fermentador:str

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fermentador = db.Column('fermentador', db.String(200))
    ciclos = db.relationship('Ciclo', backref="fermentador", order_by='Ciclo.data_inicio.desc()')


@dataclass
class Ciclo(db.Model):
    __tablename__ = "ciclo"

    id:int
    id_fermentador:int
    data_inicio:datetime
    data_inicio_formatada:str
    clone:str
    nome_ciclo:str

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    id_fermentador = db.Column('id_fermentador', db.Integer, db.ForeignKey('fermentador.id'))
    data_inicio = db.Column('data_inicio', db.Date)
    clone = db.Column(db.String(200))
    historicos = db.relationship('Historico', backref="ciclo", order_by='Historico.datetime.asc()', lazy='dynamic')

    nome_ciclo = None
    data_inicio_formatada = None

    def generateCicloName(self):
        self.data_inicio_formatada = f"{self.data_inicio}"
        self.nome_ciclo = f"{self.clone}-{self.data_inicio}-MAQUINA-{self.id_fermentador}"
    
    def generate(self):
        self.generateCicloName()

@dataclass
class Historico(db.Model):
    __tablename__ = "historico"

    id:int
    id_ciclo:int
    datetime:datetime
    PH:float
    temperatura:float
    brix:float

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    id_ciclo = db.Column('id_ciclo', db.Integer, db.ForeignKey('ciclo.id'))
    datetime = db.Column('datetime', db.DateTime)
    PH = db.Column("PH", db.Float)
    temperatura = db.Column("temperatura", db.Float)
    brix = db.Column("brix", db.Float)
