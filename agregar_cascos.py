from app import app, db
from models import Casco

with app.app_context():
    # Opcional: Limpiar cascos de prueba anteriores
    # Casco.query.delete()
    # db.session.commit()
    
    print("🔄 Cargando cascos reales de WHIP-HELMETS...")
    
    cascos = [
        Casco(
            marca='Alpinestars',
            nombre_modelo='SM5',
            tipo='motocross',
            condicion='usado',  # Cambiá según corresponda
            precio=180000,
            talle='M',
            color='',  # Agregá el color si sabés
            descripcion='Casco de motocross Alpinestars SM5.',
            imagen_principal='Alpinestars-SM5 derecha.png',
            imagenes_adicionales='Alpinestars-SM5 izquierda.png,Alpinestars-SM5 frontal.png,Alpinestars-SM5 trasera.png',
            disponible=True,
            destacado=True
        ),
        Casco(
            marca='Bell',
            nombre_modelo='Moto-9 Flex Carbono',
            tipo='motocross',
            condicion='usado',
            precio=450000,  # Es un casco premium de carbono
            talle='L',
            color='',
            descripcion='Casco Bell Moto-9 Flex de carbono.',
            imagen_principal='Bell Moto-9 Flex Carbono derecha.png',
            imagenes_adicionales='Bell Moto-9 Flex Carbono izquierda.png,Bell Moto-9 Flex Carbono frontal.png,Bell Moto-9 Flex Carbono trasera.png',
            disponible=True,
            destacado=True
        ),
        Casco(
            marca='Bell',
            nombre_modelo='Mx-9-Monster',
            tipo='motocross',
            condicion='usado',
            precio=195000,
            talle='M',
            color='Monster Energy',
            descripcion='Casco Bell MX-9 Monster Energy.',
            imagen_principal='Bell-Mx-9-Monster derecha.png',
            imagenes_adicionales='Bell-Mx-9-Monster izquierda.png,Bell Mx-9-Monster frontal.png,Bell-Mx-9-Monster trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Fly Racing',
            nombre_modelo='F2',
            tipo='motocross',
            condicion='usado',
            precio=125000,
            talle='M',
            color='',
            descripcion='Casco Fly Racing F2 Carbono/kevlar.',
            imagen_principal='Fly Racing-F2 derecha.png',
            imagenes_adicionales='Fly Racing-F2 izquierda.png,Fly Racing-F2 frontal.png,Fly Racing-F2 trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Fox',
            nombre_modelo='V1',
            tipo='motocross',
            condicion='usado',  # Típicamente V1 se vende usado
            precio=85000,
            talle='S',
            color='Azul',
            descripcion='Casco Fox V1.',
            imagen_principal='Fox-V1-Azul derecha.png',
            imagenes_adicionales='Fox-V1-Azul izquierda.png,Fox-V1-Azul frontal.png,Fox-V1-Azul trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Fox',
            nombre_modelo='V3-RS Ghost',
            tipo='motocross',
            condicion='nuevo',
            precio=320000,  # V3 RS es gama alta
            talle='M',
            color='Ghost Edition',
            descripcion='Fox V3 RS edición Ghost.',
            imagen_principal='Fox-V3-RS Ghost izquierda.png',
            imagenes_adicionales='Fox-V3-RS Ghost frontal.png,Fox-V3-RS Ghost trasera.png',
            disponible=True,
            destacado=True
        ),
        Casco(
            marca='Fox',
            nombre_modelo='V3-Moth LE Copper',
            tipo='motocross',
            condicion='usado',
            precio=340000,
            talle='S',
            color='Copper Limited Edition',
            descripcion='Fox V3 Moth edición limitada Copper.',
            imagen_principal='Fox-V3-Moth LE Copper derecha.png',
            imagenes_adicionales='Fox-V3-Moth LE Copper izquierda.png,Fox-V3-Moth LE Copper frontal.png,Fox-V3-Moth LE Copper trasera.png',
            disponible=True,
            destacado=True
        ),
        Casco(
            marca='Troy Lee Designs',
            nombre_modelo='D4',
            tipo='motocross',
            condicion='usado',
            precio=520000,  # D4 es Full Face carbono, muy premium
            talle='M',
            color='',
            descripcion='Troy Lee Designs D4 carbono.',
            imagen_principal='Troy Lee Designs-D4 derecha.png',
            imagenes_adicionales='Troy Lee Designs-D4 izquierda.png,Troy Lee Designs-D4 frontal.png,Troy Lee Designs-D4 trasera.png',
            disponible=True,
            destacado=True
        ),
        Casco(
            marca='Troy Lee Designs',
            nombre_modelo='GP',
            tipo='motocross',
            condicion='nuevo',
            precio=140000,
            talle='L',
            color='',
            descripcion='Troy Lee Designs GP.',
            imagen_principal='Troy Lee Designs-GP derecha.png',
            imagenes_adicionales='Troy Lee Designs-GP izquierda.png,Troy Lee Designs-GP frontal.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Troy Lee Designs',
            nombre_modelo='SE4 GP',
            tipo='motocross',
            condicion='usado',
            precio=280000,
            talle='XL',
            color='',
            descripcion='Troy Lee Designs SE4 versión GP.',
            imagen_principal='Troy Lee Designs-SE4 GP derecha.png',
            imagenes_adicionales='Troy Lee Designs-SE4 GP izquierda.png,Troy Lee Designs-SE4 GP frontal.png,Troy Lee Designs-SE4 GP trasera.png',
            disponible=True,
            destacado=False
        ),

        Casco(
            marca='Airoh',
            nombre_modelo='Switch Spacer',
            tipo='motocross',
            condicion='usado',
            precio=280000,
            talle='XS',
            color='',
            descripcion='Airoh Switch Spacer.',
            imagen_principal='Airoh-Switch Spacer derecha.png',
            imagenes_adicionales='Airoh-Switch Spacer izquierda.png,Airoh-Switch Spacer frontal.png,Airoh-Switch Spacer trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Alpinestars',
            nombre_modelo='SM5',
            tipo='motocross',
            condicion='usado',
            precio=280000,
            talle='XS',
            color='Tricolor',
            descripcion='Alpinestars SM5 Tricolor.',
            imagen_principal='Alpinestars-SM5 Tricolor derecha.png',
            imagenes_adicionales='Alpinestars-SM5 Tricolor izquierda.png,Alpinestars-SM5 Tricolor frontal.png,Alpinestars-SM5 Tricolor trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Bell',
            nombre_modelo='MX-9- Mips Fasthouse',
            tipo='motocross',
            condicion='usado',
            precio=280000,
            talle='S',
            color='Negro',
            descripcion='Bell Moto 9 Mips Fasthouse',
            imagen_principal='Bell-Moto-9-Mips Fasthouse derecha.png',
            imagenes_adicionales='Bell-Moto-9-Mips Fasthouse izquierda.png,Bell-Moto-9-Mips Fasthouse frontal.png,Bell-Moto-9-Mips Fasthouse trasera.png',
            disponible=True,
            destacado=False
        ),
         Casco(
            marca='Fox',
            nombre_modelo='V1',
            tipo='motocross',
            condicion='usado',  # Típicamente V1 se vende usado
            precio=85000,
            talle='L',
            color='Rojo',
            descripcion='Casco Fox V1.',
            imagen_principal='Fox-V1-Rojo derecha.png',
            imagenes_adicionales='Fox-V1-Rojo izquierda.png,Fox-V1-Rojo frontal.png,Fox-V1-Rojo trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Fox',
            nombre_modelo='V3-Motif',
            tipo='motocross',
            condicion='nuevo',
            precio=340000,
            talle='M',
            color='Motif',
            descripcion='Fox V3 Motif.',
            imagen_principal='Fox-V3-Motif derecha.png',
            imagenes_adicionales='Fox-V3-Motif izquierda.png,Fox-V3-Motif frontal.png,Fox-V3-Motif trasera.png',
            disponible=True,
            destacado=True
        ),
        Casco(
            marca='Troy Lee Designs',
            nombre_modelo='SE4 GP Pinstripe-Carbono',
            tipo='motocross',
            condicion='usado',
            precio=280000,
            talle='M',
            color='Pinstripe-Carbono',
            descripcion='Troy Lee Designs SE4 versión GP Pinstripe-Carbono.',
            imagen_principal='Troy Lee Designs-SE4-Pinstripe-Carbono derecha.png',
            imagenes_adicionales='Troy Lee Designs-SE4-Pinstripe-Carbono izquierda.png,Troy Lee Designs-SE4-Pinstripe-Carbono frontal.png,Troy Lee Designs-SE4-Pinstripe-Carbono trasera.png',
            disponible=True,
            destacado=False
        ),
        Casco(
            marca='Troy Lee Designs',
            nombre_modelo='SE5 GP Carbono',
            tipo='motocross',
            condicion='usado',
            precio=280000,
            talle='M',
            color='Carbono',
            descripcion='Troy Lee Designs SE5 versión GP Carbono.',
            imagen_principal='Troy Lee Designs-SE5-Carbono derecha.png',
            imagenes_adicionales='Troy Lee Designs-SE5-Carbono izquierda.png,Troy Lee Designs-SE5-Carbono frontal.png,Troy Lee Designs-SE5-Carbono trasera.png',
            disponible=True,
            destacado=False
        ),
     
    ]
    
    for casco in cascos:
        db.session.add(casco)
    
    db.session.commit()
    
    print(f"✅ Se cargaron {len(cascos)} cascos de WHIP-HELMETS!")
    print("\n📋 Resumen del catálogo:")
    print(f"   - Cascos nuevos: {len([c for c in cascos if c.condicion == 'nuevo'])}")
    print(f"   - Cascos usados: {len([c for c in cascos if c.condicion == 'usado'])}")
    print(f"   - Cascos destacados: {len([c for c in cascos if c.destacado])}")
    print("\n💰 Rango de precios: ${min([c.precio for c in cascos]):,.0f} - ${max([c.precio for c in cascos]):,.0f}")
    print("\n🏷️  Marcas en catálogo:")
    marcas = set([c.marca for c in cascos])
    for marca in marcas:
        cantidad = len([c for c in cascos if c.marca == marca])
        print(f"   - {marca}: {cantidad} cascos")
    print("\n🌐 Visitá http://127.0.0.1:5000 para ver el catálogo")
