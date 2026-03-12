from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Casco(db.Model):
    __tablename__ = 'cascos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20))
    condicion = db.Column(db.String(10), nullable=False)
    
    precio = db.Column(db.Float, nullable=False)
    precio_1_cuota = db.Column(db.Float, nullable=True)
    precio_3_cuotas = db.Column(db.Float, nullable=True)
    
    descripcion = db.Column(db.Text)
    talle = db.Column(db.String(10))
    color = db.Column(db.String(30))
    
    imagen_principal = db.Column(db.String(200))
    imagenes_adicionales = db.Column(db.Text)
    instagram_url = db.Column(db.String(300))
    
    disponible = db.Column(db.Boolean, default=True)
    destacado = db.Column(db.Boolean, default=False)
    reservado = db.Column(db.Boolean, default=False)  # NUEVO
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Casco {self.marca} {self.nombre_modelo}>'
    
    def get_imagenes_lista(self):
        if self.imagenes_adicionales:
            return self.imagenes_adicionales.split(',')
        return []


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Datos personales
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), nullable=False)
    telefono = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100))
    
    # Entrega
    tipo_entrega = db.Column(db.String(10), nullable=False)  # 'retiro' o 'envio'
    codigo_postal = db.Column(db.String(10))
    provincia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    
    # Pago
    metodo_pago = db.Column(db.String(20))  # 'mercadopago' o 'transferencia'
    estado = db.Column(db.String(20), default='pendiente')  # pendiente / confirmado / rechazado
    mp_payment_id = db.Column(db.String(100))  # ID de MercadoPago si aplica
    
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relación con items
    items = db.relationship('ItemPedido', backref='pedido', cascade='all, delete-orphan')

    
    def __repr__(self):
        return f'<Pedido #{self.id} - {self.nombre} {self.apellido}>'


class ItemPedido(db.Model):
    __tablename__ = 'items_pedido'
    
    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedidos.id'), nullable=False)
    casco_id = db.Column(db.Integer, db.ForeignKey('cascos.id'), nullable=False)
    precio = db.Column(db.Float, nullable=False)  # precio efectivo/transferencia
    
    casco = db.relationship('Casco')
    
    def __repr__(self):
        return f'<ItemPedido pedido={self.pedido_id} casco={self.casco_id}>'
