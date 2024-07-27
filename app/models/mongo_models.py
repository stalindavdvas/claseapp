from pymongo import MongoClient

class Auditoria:
    def __init__(self, usuario_id, fecha, estado, metodo_auth):
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.estado = estado
        self.metodo_auth = metodo_auth

    def to_dict(self):
        return {
            'usuario_id': self.usuario_id,
            'fecha': self.fecha,
            'estado': self.estado,
            'metodo_auth': self.metodo_auth
        }
