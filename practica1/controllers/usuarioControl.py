from flask import current_app, jsonify, make_response, request
import jwt
from datetime import datetime, timedelta
from functools import wraps
from models.usuario import Usuario  # Asumiendo que este es el modelo Usuario
import hashlib
import uuid
from app import db

class UsuarioControl:

    def listarUsuarios(self):
        return Usuario.query.all()
    
    def saveUsuario(self, data):
        usuarioExistente = Usuario.query.filter_by(username=data['username']).first()
        if usuarioExistente:
            return -1
        else:
            # Encripta la contraseña utilizando SHA-256
            clave_encriptada = hashlib.sha256(data['clave'].encode()).hexdigest()
            
            # Crea un nuevo usuario con la contraseña encriptada
            usuario = Usuario(username=data['username'], clave=clave_encriptada, external_id=uuid.uuid4())
            
            db.session.add(usuario)
            db.session.commit()
            return usuario.id
        

    def login(self, data):
        usuarioA = Usuario.query.filter_by(username=data["username"]).first()
        if usuarioA:
            clave_encriptada_usuario = hashlib.sha256(data["clave"].encode()).hexdigest()
            if (usuarioA.clave == clave_encriptada_usuario):
                token = jwt.encode(
                    {
                        "external": usuarioA.external_id,
                        "exp": datetime.utcnow() + timedelta(minutes=60)
                    },
                    key=current_app.config["SECRET_KEY"],
                    algorithm="HS512"
                )
                usuario = Usuario()
                usuario.copy()
                                
                info = {
                    "token": token,  # Decodifica el token byte a str
                    "user": data['username']
                }
                return info
            else:
                return -10
        else:
            return -8