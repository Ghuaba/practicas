import uuid
from app import db
from sqlalchemy.sql import func
from .detalle_factura import DetalleFactura
from .factura import Factura  # Importa la clase Factura al final

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    facturas = db.relationship('Factura', secondary='detalle_factura', backref='productos')
    lote = db.relationship('Lote', backref='producto', lazy=True)


    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())

    @property
    def serialize(self):
        return {
            'nombre': self.nombre,
            'external_id': self.external_id
#            'lote' : [i.serialize for i in self.lote]

        }

    def copy(self):
        new_producto = Producto(
            id=self.id,
            nombre=self.nombre,
            external_id=self.external_id
        )
        return new_producto
