from flask import Blueprint, request, jsonify,current_app
from flask_cors import CORS
from ..factories.postgres_factory import PostgresFactory
from ..factories.mongo_factory import MongoFactory
from ..models.postgres_models import db
from datetime import datetime
from bson.json_util import dumps
import os
import pytz
import jwt
import requests
from bson import json_util,ObjectId
import json
bp = Blueprint('api', __name__)
CORS(bp, resources={r"/*": {"origins": "*"}})

postgres_factory = PostgresFactory()
mongo_factory = MongoFactory()
AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://auth_service:5001')
# Usuarios CRUD

@bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.json
    Usuario = postgres_factory.create_model('Usuario')
    nuevo_usuario = Usuario(**data)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario creado exitosamente', 'id': nuevo_usuario.id}), 201

@bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    Usuario = postgres_factory.create_model('Usuario')
    usuarios = Usuario.query.all()
    return jsonify([{
        'id': u.id,
        'nombre': u.nombre,
        'apellido': u.apellido,
        'dni': u.dni,
        'correo': u.correo,
        'celular': u.celular,
        'rol': u.rol
    } for u in usuarios]), 200

@bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    Usuario = postgres_factory.create_model('Usuario')
    usuario = Usuario.query.get_or_404(id)
    return jsonify({
        'id': usuario.id,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'dni': usuario.dni,
        'correo': usuario.correo,
        'celular': usuario.celular,
        'rol': usuario.rol
    }), 200

@bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.json
    Usuario = postgres_factory.create_model('Usuario')
    usuario = Usuario.query.get_or_404(id)
    for key, value in data.items():
        setattr(usuario, key, value)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario actualizado exitosamente'}), 200

@bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    Usuario = postgres_factory.create_model('Usuario')
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Usuario eliminado exitosamente'}), 200

# Cursos CRUD

@bp.route('/cursos', methods=['POST'])
def crear_curso():
    data = request.json
    Curso = postgres_factory.create_model('Curso')
    nuevo_curso = Curso(**data)
    db.session.add(nuevo_curso)
    db.session.commit()
    return jsonify({'mensaje': 'Curso creado exitosamente', 'id': nuevo_curso.id}), 201

@bp.route('/cursos', methods=['GET'])
def obtener_cursos():
    Curso = postgres_factory.create_model('Curso')
    cursos = Curso.query.all()
    return jsonify([{
        'id': c.id,
        'nombre': c.nombre
    } for c in cursos]), 200

@bp.route('/cursos/<int:id>', methods=['GET'])
def obtener_curso(id):
    Curso = postgres_factory.create_model('Curso')
    curso = Curso.query.get_or_404(id)
    return jsonify({
        'id': curso.id,
        'nombre': curso.nombre
    }), 200

@bp.route('/cursos/<int:id>', methods=['PUT'])
def actualizar_curso(id):
    data = request.json
    Curso = postgres_factory.create_model('Curso')
    curso = Curso.query.get_or_404(id)
    curso.nombre = data['nombre']
    db.session.commit()
    return jsonify({'mensaje': 'Curso actualizado exitosamente'}), 200

@bp.route('/cursos/<int:id>', methods=['DELETE'])
def eliminar_curso(id):
    Curso = postgres_factory.create_model('Curso')
    curso = Curso.query.get_or_404(id)
    db.session.delete(curso)
    db.session.commit()
    return jsonify({'mensaje': 'Curso eliminado exitosamente'}), 200

# Notas CRUD

@bp.route('/notas', methods=['POST'])
def crear_nota():
    data = request.json
    Nota = postgres_factory.create_model('Nota')
    nueva_nota = Nota(**data)
    db.session.add(nueva_nota)
    db.session.commit()
    return jsonify({'mensaje': 'Nota creada exitosamente', 'id': nueva_nota.id}), 201

@bp.route('/notas', methods=['GET'])
def obtener_notas():
    Nota = postgres_factory.create_model('Nota')
    notas = Nota.query.all()
    return jsonify([{
        'id': n.id,
        'nota': n.nota,
        'idusuario': n.idusuario,
        'idcurso': n.idcurso
    } for n in notas]), 200

@bp.route('/notas/<int:id>', methods=['GET'])
def obtener_nota(id):
    Nota = postgres_factory.create_model('Nota')
    nota = Nota.query.get_or_404(id)
    return jsonify({
        'id': nota.id,
        'nota': nota.nota,
        'idusuario': nota.idusuario,
        'idcurso': nota.idcurso
    }), 200

@bp.route('/notas/<int:id>', methods=['PUT'])
def actualizar_nota(id):
    data = request.json
    Nota = postgres_factory.create_model('Nota')
    nota = Nota.query.get_or_404(id)
    for key, value in data.items():
        setattr(nota, key, value)
    db.session.commit()
    return jsonify({'mensaje': 'Nota actualizada exitosamente'}), 200

@bp.route('/notas/<int:id>', methods=['DELETE'])
def eliminar_nota(id):
    Nota = postgres_factory.create_model('Nota')
    nota = Nota.query.get_or_404(id)
    db.session.delete(nota)
    db.session.commit()
    return jsonify({'mensaje': 'Nota eliminada exitosamente'}), 200

# Login (se mantiene igual)
def json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return str(obj)
    return json_util.default(obj)

"""@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    Usuario = postgres_factory.create_model('Usuario')
    usuario = Usuario.query.filter_by(correo=data['correo']).first()

    if usuario:
        print(f"Usuario encontrado: {usuario.correo}, DNI: {usuario.dni}")
    else:
        print("Usuario no encontrado")

    estado = 'fallido'
    dni = 'desconocido'
    rol = None
    fecha = datetime.now()
    fecha_formateada = fecha.strftime('%d/%m/%Y %H:%M:%S')

    if usuario:
        print(f"Contraseña proporcionada: {data['passwd']}")
        print(f"Contraseña almacenada: {usuario.passwd}")
        if usuario.passwd == data['passwd']:
            estado = 'exitoso'
            dni = usuario.dni
            rol = usuario.rol
        else:
            print("Contraseña incorrecta")

    Auditoria = mongo_factory.create_model('Auditoria')
    log = Auditoria(
        usuario_id=usuario.id if usuario else None,  # Cambiado a usuario.id en lugar de data['id']
        fecha=fecha_formateada,
        estado=estado
    )

    mongo_db = mongo_factory.create_connection(current_app)
    if not mongo_db:
        return jsonify({'mensaje': 'Error al conectar a MongoDB'}), 500

    mongo_db.auditoria.insert_one(log.to_dict())

    if estado == 'exitoso':
        return jsonify({'mensaje': 'Login exitoso', 'rol': rol}), 200
    else:
        return jsonify({'mensaje': 'Login fallido'}), 401"""
# Login
# JSON encoder for BSON types
def json_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, ObjectId):
        return str(obj)
    return dumps(obj)

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    Usuario = postgres_factory.create_model('Usuario')
    estado = 'fallido'
    dni = 'desconocido'
    rol = None
    token = None
    # Define la zona horaria deseada
    timezone = pytz.timezone('America/Guayaquil')
    # Obtén la hora actual en UTC
    now_utc = datetime.utcnow()
    # Convierte la hora UTC a la zona horaria deseada
    now_local = pytz.utc.localize(now_utc).astimezone(timezone)
    # Usa la hora local en tu aplicación
    fecha_formateada = now_local.strftime('%d/%m/%Y %H:%M:%S')
    metodo_auth = 'tradicional'
    usuario = None

    if 'sso_token' in data:  # Si se proporciona un token SSO
        # Verificar el token con el servicio de autenticación
        response = requests.post(f'{AUTH_SERVICE_URL}/verify', json={'token': data['sso_token']})
        if response.status_code == 200:
            sso_data = response.json()
            usuario = Usuario.query.filter_by(correo=sso_data['user_id']).first()
            if usuario:
                estado = 'exitoso'
                dni = usuario.dni
                rol = usuario.rol
                metodo_auth = 'sso'
                # No generamos un nuevo token aquí ya que estamos utilizando el token SSO
                token = data['sso_token']
    else:  # Autenticación tradicional
        auth_response = requests.post(f'{AUTH_SERVICE_URL}/auth', json={
            'username': data['correo'],
            'password': data['passwd']
        })

        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            token = auth_data.get('token')

            # Verificar el token devuelto por el servicio de autenticación
            verify_response = requests.post(f'{AUTH_SERVICE_URL}/verify', json={'token': token})
            if verify_response.status_code == 200:
                usuario = Usuario.query.filter_by(correo=data['correo']).first()
                if usuario:
                    estado = 'exitoso'
                    dni = usuario.dni
                    rol = usuario.rol

    # Registrar en la auditoría
    Auditoria = mongo_factory.create_model('Auditoria')
    log = Auditoria(
        usuario_id=usuario.id if usuario else None,
        fecha=fecha_formateada,
        estado=estado,
        metodo_auth=metodo_auth
    )

    mongo_db = mongo_factory.create_connection(current_app)
    if not mongo_db:
        return jsonify({'mensaje': 'Error al conectar a MongoDB'}), 500

    mongo_db.auditoria.insert_one(log.to_dict())

    if estado == 'exitoso':
        return jsonify({'mensaje': 'Login exitoso', 'rol': rol, 'token': token}), 200
    else:
        return jsonify({'mensaje': 'Login fallido'}), 401


# Convertir la respuesta JSON para que las fechas se vean correctamente
@bp.after_request
def after_request(response):
    if response.content_type == 'application/json':
        response_data = response.get_json()
        response.data = json.dumps(response_data, default=json_encoder)
    return response

@bp.route('/auditoria', methods=['GET'])
def obtener_auditoria():
    mongo_db = mongo_factory.create_connection(current_app)
    auditoria_collection = mongo_db.auditoria

    # Obtener todos los registros de auditoría
    registros = list(auditoria_collection.find())

    # Convertir ObjectId a string para que sea serializable
    for registro in registros:
        registro['_id'] = str(registro['_id'])

    # Usar json_util para manejar tipos de datos de MongoDB
    return json.loads(json_util.dumps({'registros': registros})), 200

@bp.route('/auditoria-combinada', methods=['GET'])
def obtener_auditoria_combinada():
    mongo_db = mongo_factory.create_connection(current_app)
    Usuario = postgres_factory.create_model('Usuario')
    Auditoria = mongo_factory.create_model('Auditoria')

    usuarios = {usuario.id: usuario for usuario in Usuario.query.all()}
    auditorias = mongo_db.auditoria.find()

    registros_combinados = []
    for aud in auditorias:
        usuario = usuarios.get(aud['usuario_id'])
        if usuario:
            registros_combinados.append({
                'usuario': usuario.nombre + ' ' + usuario.apellido,
                'dni': usuario.dni,
                'fecha': aud['fecha'],
                'estado': aud['estado'],
                'metodoAutenticacion': aud.get('metodo_auth', 'desconocido')
            })

    return jsonify({'registros_combinados': registros_combinados}), 200

