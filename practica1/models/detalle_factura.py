import uuid

from app import db
from sqlalchemy.sql import func

class DetalleFactura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    external_id = db.Column(db.VARCHAR(60), default=str(uuid.uuid4())) 
    created_at = db.Column(db.DateTime, default=func.now())
    updated_at = db.Column(db.DateTime, default=func.now(), onupdate=func.now())
