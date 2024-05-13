import uuid
from app import db
import datetime
from sqlalchemy.sql import func
from .estadoLote import EstadoLote



class Lote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Boolean, default=True)
    estadoLote = db.Column(db.Enum(EstadoLote))
    codigo = db.Column(db.String(50), nullable=False)
    fecha_emision = db.Column(db.DateTime, default=func.now())
    fecha_caducidad = db.Column(db.DateTime, default= func.now())
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Double, nullable = False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    
    #producto = db.relationship('Producto', back_populates='lote')

    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))


    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def serialize(self):
        return {
            'codigo': self.codigo,
            'estado' : 1 if self.estado else 0,
            'estadoLote': self.estadoLote.value,
            'fecha_emision': self.fecha_emision,
            'fecha_caducidad': self.fecha_caducidad,
#            'producto_id' : [i.serialize for i in self.producto],
            'producto_id': self.producto.serialize,  # Agregar información del producto
            'cantidad': self.cantidad,
            'external_id': self.external_id
        }
    

    def copy(self):
        new_lote = Lote(
            id=self.id,
            estado = self.estado,
            codigo = self.codigo,
            estadoLote = self.estadoLote,
            fecha_emision=self.fecha_emision,
            fecha_caducidad=self.fecha_caducidad,
            cantidad = self.cantidad,
            producto_id = self.producto_id,
            external_id=self.external_id
        )
        return new_lote
