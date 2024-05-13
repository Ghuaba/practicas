import uuid
from app import db
import datetime
from sqlalchemy.sql import func
#from .detalle_factura import DetalleFactura
#from .producto import Producto  # Importa la clase Producto al final

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_emision = db.Column(db.DateTime, default=func.now())
    total = db.Column(db.Float, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
#    productos = db.relationship('Producto', secondary='detalle_factura', backref='facturas')
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))

    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def serialize(self):
        return {
            'fecha_emision': self.fecha_emision,
            'total': self.total,
            'usuario_id': self.usuario_id,
            'productos': [producto.serialize for producto in self.productos],
            'external_id': self.external_id
        }

    def copy(self):
        new_factura = Factura(
            id=self.id,
            fecha_emision=self.fecha_emision,
            total=self.total,
            usuario_id=self.usuario_id,
            external_id=self.external_id,
        )
        return new_factura
