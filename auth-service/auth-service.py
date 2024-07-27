"""from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:stalin@postgres:5432/notas'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
CORS(app)

# Modelo de usuario (ajustado para no crear tablas)
class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(20))
    rol = db.Column(db.String(50), nullable=False)

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json

    if 'sso_token' in data:
        # Verificar el token SSO
        token = data['sso_token']
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = Usuario.query.filter_by(correo=decoded['user_id']).first()
            if user:
                return jsonify({'mensaje': 'Login exitoso', 'rol': user.rol, 'token': token}), 200
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'Invalid token'}), 401
    else:
        # Autenticación tradicional
        user = Usuario.query.filter_by(correo=data['username']).first()
        if user and user.passwd == data['password']:
            token = jwt.encode({
                'user_id': user.correo,
                'role': user.rol,
                'exp': datetime.utcnow() + timedelta(seconds=30) #aqui podemos cambiar la duracion del token
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token, 'rol': user.rol}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/verify', methods=['POST'])
def verify_token():
    data = request.json
    token = data.get('token')

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify(decoded), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)"""
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:stalin@postgres:5432/notas'
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)
CORS(app)

# Definir la IP en una variable
BASE_URL = 'http://192.168.100.230:3000'  # Reemplazo con la IP de la máquina
# Modelo de usuario (ajustado para no crear tablas)
class Usuario(db.Model):
    __tablename__ = 'usuarios'  # Nombre de la tabla en PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    passwd = db.Column(db.String(255), nullable=False)
    celular = db.Column(db.String(20))
    rol = db.Column(db.String(50), nullable=False)

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.json

    if 'sso_token' in data:
        # Verificar el token SSO
        token = data['sso_token']
        try:
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = Usuario.query.filter_by(correo=decoded['user_id']).first()
            if user:
                return jsonify({'mensaje': 'Login exitoso', 'rol': user.rol, 'token': token}), 200
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({'mensaje': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensaje': 'Invalid token'}), 401
    else:
        # Autenticación tradicional
        user = Usuario.query.filter_by(correo=data['username']).first()
        if user and user.passwd == data['password']:
            token = jwt.encode({
                'user_id': user.correo,
                'role': user.rol,
                'exp': datetime.utcnow() + timedelta(seconds=3600)  # Duración del token de 1 hora
            }, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token, 'rol': user.rol}), 200
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/generate-url', methods=['POST'])
def generate_url():
    data = request.json
    token = data.get('token')
    if token:
        url = f"{BASE_URL}?token={token}"
        return jsonify({'url': url}), 200
    return jsonify({'message': 'Token not provided'}), 400

@app.route('/current-user', methods=['GET'])
def current_user():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token not provided'}), 401

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user = Usuario.query.filter_by(correo=decoded['user_id']).first()
        if user:
            return jsonify({
                'id': user.id,
                'nombre': user.nombre,
                'apellido': user.apellido,
                'dni': user.dni,
                'correo': user.correo,
                'celular': user.celular,
                'rol': user.rol
            }), 200
        return jsonify({'message': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401


@app.route('/verify', methods=['POST'])
def verify_token():
    data = request.json
    token = data.get('token')

    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify(decoded), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)


