import uuid
from app import db
import datetime
from sqlalchemy.sql import func
from .factura import Factura

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique = True)
    clave = db.Column(db.String(150))
    estado = db.Column(db.Boolean, default=True)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))

    created_at = db.Column(db.DateTime, default = func.now())
    updated_at = db.Column(db.DateTime, default = func.now(), onupdate = func.now())
    factura = db.relationship('Factura', backref='usuario', lazy=True)

    @property
    def serialize (self):
        return{
            'username' : self.username,
#            'clave' : self.clave,
            'estado' : 1 if self.estado else 0,
            'external_id' :self.external_id
        }

    
    def copy(self):
        new_usuario = Usuario(
            id=self.id,
            username=self.username,
            clave=self.clave,
            estado=self.estado,
            external_id=self.external_id,
        )
        return new_usuario












'''
    def getPersona(self, persona_id):
        from models.persona import Persona
        return Persona.query.filter_by(id = persona_id).first()
'''


