from app import app, db
from models import Casco

with app.app_context():
    # Ver cascos vendidos/no disponibles
    cascos = Casco.query.filter_by(disponible=False).all()
    
    if not cascos:
        print("✅ No hay cascos marcados como vendidos")
    else:
        print("📋 Cascos NO DISPONIBLES:")
        for i, casco in enumerate(cascos, 1):
            print(f"{i}. ID: {casco.id} - {casco.marca} {casco.nombre_modelo}")
        
        # Elegir cuál volver a marcar como disponible
        id_casco = int(input("\n¿ID del casco a REACTIVAR? "))
        
        casco = Casco.query.get(id_casco)
        if casco:
            casco.disponible = True
            db.session.commit()
            print(f"✅ {casco.marca} {casco.nombre_modelo} ahora está DISPONIBLE nuevamente")
        else:
            print("❌ Casco no encontrado")
