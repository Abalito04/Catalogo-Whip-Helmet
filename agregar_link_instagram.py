from app import app, db
from models import Casco

with app.app_context():
    # Ver todos los cascos
    cascos = Casco.query.all()
    
    print("📋 Cascos disponibles:")
    for i, casco in enumerate(cascos, 1):
        link = casco.instagram_url or "Sin link"
        print(f"{i}. ID: {casco.id} - {casco.marca} {casco.nombre_modelo} - Link: {link}")
    
    # Elegir casco
    id_casco = int(input("\n¿ID del casco para agregar link de Instagram? "))
    
    casco = Casco.query.get(id_casco)
    if casco:
        print(f"\nCasco seleccionado: {casco.marca} {casco.nombre_modelo}")
        instagram_link = input("Pegá el link del post de Instagram: ")
        
        casco.instagram_url = instagram_link
        db.session.commit()
        print(f"✅ Link de Instagram agregado correctamente!")
    else:
        print("❌ Casco no encontrado")
