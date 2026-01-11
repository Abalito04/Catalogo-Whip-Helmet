# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Casco(db.Model):
    __tablename__ = 'cascos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_modelo = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(20))  # integral, abierto, modular, jet
    condicion = db.Column(db.String(10), nullable=False)  # 'nuevo' o 'usado'
    
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    talle = db.Column(db.String(10))
    color = db.Column(db.String(30))
    
    # Imágenes (rutas relativas)
    imagen_principal = db.Column(db.String(200))
    imagenes_adicionales = db.Column(db.Text)  # Separadas por comas

    # Link de Instagram
    instagram_url = db.Column(db.String(300))  # URL del post de Instagram
    
    # Estados
    disponible = db.Column(db.Boolean, default=True)
    destacado = db.Column(db.Boolean, default=False)
    fecha_agregado = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Casco {self.marca} {self.nombre_modelo}>'
    
    def get_imagenes_lista(self):
        """Devuelve lista de imágenes adicionales"""
        if self.imagenes_adicionales:
            return self.imagenes_adicionales.split(',')
        return []
