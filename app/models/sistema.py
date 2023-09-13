from sqlalchemy import(
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.types import(
    Boolean,
    DateTime
)
from sqlalchemy.orm import(
    relationship,
    Session
)

from datetime import datetime
from typing import Type

from app.core.database import Base
from app.models.base import ModelBase

from dataclasses import dataclass


@dataclass
class Disciplina(ModelBase, Base):
    __tablename__ = "Disciplina"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name: str = Column(String(255))
    icon: str = Column(String(255))
    description: str = Column(String(255))
    date_created: datetime = Column(DateTime, default=datetime.utcnow())
    assuntos = relationship('Assunto', backref='Disciplina')


    @classmethod
    def list_by_id_moar(cls, session, id):
        try:
            temp = session.query(cls).filter_by(id=id).first()
            if temp:
                data = {
                    'id': temp.id,
                    'name': temp.name,
                    'icon': temp.icon,
                    'description': temp.description,
                }
                assuntos_data = []
                if len(temp.assuntos)>0:
                    for assunto in temp.assuntos:
                        assuntos_data.append({
                            'id': assunto.id,
                            'description': assunto.description,
                            'disciplina_id': assunto.disciplina_id,
                            'total_questions': len(assunto.perguntas)
                        })
                data.update({
                    'assuntos': assuntos_data
                })
                return data
        except Exception as err:
            print(f'exp Disciplina.list_by_id_moar - {err}')
        return False
    

@dataclass
class Assunto(ModelBase, Base):
    __tablename__ = "Assunto"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255))
    disciplina_id = Column(Integer, ForeignKey("Disciplina.id"), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow())
    perguntas = relationship('Pergunta', backref='Assunto')
    #disciplina = relationship('Disciplina', foreign_keys='Assunto.disciplina_id')


    @classmethod
    def list_by_id_moar(cls, session, id):
        try:
            temp = session.query(Assunto).filter_by(id=id).first()
            if temp:
                data = {
                    'id': temp.id,
                    'description': temp.description,
                    'disciplina_id': temp.disciplina_id,
                    'date_created': temp.date_created,
                    'disciplina_data': {
                        'id': temp.Disciplina.id,
                        'name': temp.Disciplina.name,
                        'description': temp.Disciplina.description,
                        'date_created': temp.Disciplina.date_created,
                    }
                }
                questions_data = []
                if len(temp.perguntas)>0:
                    for pergunta in temp.perguntas:
                        questions_data.append({
                            'id': pergunta.id,
                            'question': pergunta.question,
                            'correct': pergunta.correct,
                            'assunto_id': pergunta.assunto_id,
                            'date_created': pergunta.date_created,
                        })
                data.update({
                    'questions': questions_data
                })
                return data
        except Exception as err:
            print(f'exp Assunto.list_by_id_moar - {err}')
        return False



@dataclass
class Pergunta(ModelBase, Base):
    __tablename__ = "Pergunta"
    id: int = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question: str = Column(String(255))
    #key = Column(String(255))
    correct: bool = Column(Boolean, nullable=False)
    assunto_id: int = Column(Integer, ForeignKey("Assunto.id"), nullable=False)
    date_created: datetime = Column(DateTime, default=datetime.utcnow())
    #alternative_answers = relationship('Resposta', backref='Pergunta')




##??? deletar?
# class Resposta(ModelBase, Base):
#     __tablename__ = "Resposta"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     alternative = Column(String(255), nullable=False)
#     correct = Column(Boolean, nullable=False)
#     question_id = Column(Integer, ForeignKey("Pergunta.id"), nullable=False)
#     date_created = Column(DateTime, default=datetime.utcnow())