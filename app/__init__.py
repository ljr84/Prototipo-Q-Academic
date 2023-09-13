from flask import Flask, jsonify, redirect
from config import Config
from flask_sqlalchemy import SQLAlchemy


from app.core.database import(
    SessionLocal,
    engine,
    Base
)

from sqlalchemy.ext.declarative import declarative_base




def create_app():
    app = Flask(
        __name__,
        static_url_path='/static',
        static_folder='static',
        template_folder='templates'
    )
    app.config.from_object(Config)
    return app




app = create_app()

db = SQLAlchemy(app)


Base = declarative_base()
Base.metadata.create_all(bind=engine, checkfirst=True)






from app import(
    views,
    forms
)


db.create_all()

