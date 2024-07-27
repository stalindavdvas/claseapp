from .database_factory import DatabaseFactory
from ..models.mongo_models import Auditoria
from pymongo import MongoClient

class MongoFactory(DatabaseFactory):
    def create_connection(self, app):
        client = MongoClient(app.config['MONGO_URI'])
        return client.log

    def create_model(self, model_name):
        if model_name == 'Auditoria':
            return Auditoria
        else:
            raise ValueError(f"Modelo no reconocido: {model_name}")