from .database_factory import DatabaseFactory
from ..models.postgres_models import db, Usuario, Curso, Nota
from flask_sqlalchemy import SQLAlchemy

class PostgresFactory(DatabaseFactory):
    def create_connection(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@postgres:5432/notas'
        db.init_app(app)
        return db

    def create_model(self, model_name):
        if model_name == 'Usuario':
            return Usuario
        elif model_name == 'Curso':
            return Curso
        elif model_name == 'Nota':
            return Nota
        else:
            raise ValueError(f"Modelo no reconocido: {model_name}")