from app import app, db
from models import Casco

with app.app_context():
    print("➕ Agregar nuevo casco\n")
    
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    tipo = input("Tipo (motocross/integral/abierto/modular): ")
    condicion = input("Condición (nuevo/usado): ")
    precio = float(input("Precio: "))
    talle = input("Talle (S/M/L/XL/XXL): ")
    color = input("Color: ")
    descripcion = input("Descripción: ")
    
    # Construir nombre de imágenes
    nombre_base = f"{marca}-{modelo}"
    if color:
        nombre_base = f"{marca}-{modelo} {color}"
    
    nuevo_casco = Casco(
        marca=marca,
        nombre_modelo=modelo,
        tipo=tipo,
        condicion=condicion,
        precio=precio,
        talle=talle,
        color=color,
        descripcion=descripcion,
        imagen_principal=f"{nombre_base} frontal.png",
        imagenes_adicionales=f"{nombre_base} trasera.png,{nombre_base} izquierda.png,{nombre_base} derecha.png",
        disponible=True,
        destacado=False
    )
    
    db.session.add(nuevo_casco)
    db.session.commit()
    
    print(f"\n✅ {marca} {modelo} agregado exitosamente!")
    print(f"📸 No olvides agregar las imágenes en: static/images/cascos/")
