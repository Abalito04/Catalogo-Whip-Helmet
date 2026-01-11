from app import app, db
from models import Casco

with app.app_context():
    # Ver todos los cascos disponibles
    cascos = Casco.query.filter_by(disponible=True).all()
    
    print("📋 Cascos disponibles:")
    for i, casco in enumerate(cascos, 1):
        print(f"{i}. ID: {casco.id} - {casco.marca} {casco.nombre_modelo} (${casco.precio})")
    
    # Elegir cuál marcar como vendido
    id_casco = int(input("\n¿ID del casco vendido? "))
    
    casco = Casco.query.get(id_casco)
    if casco:
        casco.disponible = False
        db.session.commit()
        print(f"✅ {casco.marca} {casco.nombre_modelo} marcado como VENDIDO")
    else:
        print("❌ Casco no encontrado")
