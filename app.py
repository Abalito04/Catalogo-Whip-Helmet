# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Casco, Pedido, ItemPedido
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import cloudinary
import cloudinary.uploader
from functools import wraps
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'clave-local-de-desarrollo')
csrf = CSRFProtect(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Necesitás iniciar sesión para acceder.'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

database_url = os.getenv('DATABASE_URL', 'sqlite:///cascos.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# -------------------------------------------------------
# REMBG
# -------------------------------------------------------
def remover_fondo_rembg(file):
    try:
        from rembg import remove
        print("🪄 Removiendo fondo con rembg...")
        img_bytes = file.read()
        file.seek(0)
        img_sin_fondo = remove(img_bytes)
        print("✅ Fondo removido correctamente")
        return img_sin_fondo, None
    except Exception as e:
        print(f"❌ Error removiendo fondo: {e}")
        return None, str(e)


def precargar_modelo_rembg():
    try:
        print("⏳ Pre-cargando modelo rembg...")
        from rembg import new_session
        new_session("u2net")
        print("✅ Modelo rembg listo")
    except Exception as e:
        print(f"⚠️ No se pudo pre-cargar rembg: {e}")


precargar_modelo_rembg()


# -------------------------------------------------------
# HELPER: subir imagen con o sin rembg
# -------------------------------------------------------
def subir_imagen(file, aplicar_rembg=False):
    if aplicar_rembg:
        img_procesada, error = remover_fondo_rembg(file)
        if img_procesada:
            return cloudinary.uploader.upload(
                img_procesada, folder="whip-helmets", timeout=60, format="png"
            )
        else:
            flash(f'No se pudo remover el fondo: {error}. Se subió la imagen original.', 'warning')
    return cloudinary.uploader.upload(file, folder="whip-helmets", timeout=60)


# -------------------------------------------------------
# HELPER: número de items en carrito (para navbar)
# -------------------------------------------------------
def get_carrito_count():
    return len(session.get('carrito', []))

app.jinja_env.globals['get_carrito_count'] = get_carrito_count


# -------------------------------------------------------
# RUTAS PRINCIPALES
# -------------------------------------------------------
@app.route('/')
def index():
    condicion_filtro = request.args.get('condicion')
    tipo_filtro = request.args.get('tipo')
    marca_filtro = request.args.get('marca')

    query = Casco.query.filter_by(disponible=True)

    if condicion_filtro:
        query = query.filter_by(condicion=condicion_filtro)
    if tipo_filtro:
        query = query.filter_by(tipo=tipo_filtro)
    if marca_filtro:
        query = query.filter_by(marca=marca_filtro)

    cascos = query.order_by(Casco.destacado.desc(), Casco.fecha_agregado.desc()).all()

    marcas = db.session.query(Casco.marca).distinct().filter_by(disponible=True).all()
    marcas = [m[0] for m in marcas]

    tipos = db.session.query(Casco.tipo).distinct().filter_by(disponible=True).all()
    tipos = [t[0] for t in tipos if t[0]]

    return render_template('index.html',
                           cascos=cascos,
                           marcas=marcas,
                           tipos=tipos,
                           filtro_actual={'condicion': condicion_filtro,
                                          'tipo': tipo_filtro,
                                          'marca': marca_filtro})


@app.route('/producto/<int:id>')
def producto(id):
    casco = Casco.query.get_or_404(id)
    return render_template('producto.html', casco=casco)


# -------------------------------------------------------
# RUTAS CARRITO
# -------------------------------------------------------
@app.route('/carrito/agregar/<int:casco_id>', methods=['POST'])
def agregar_al_carrito(casco_id):
    casco = Casco.query.get_or_404(casco_id)

    if not casco.disponible:
        flash('Este casco ya no está disponible.', 'error')
        return redirect(url_for('producto', id=casco_id))

    carrito = session.get('carrito', [])

    # Verificar si ya está en el carrito
    if casco_id in carrito:
        flash(f'{casco.marca} {casco.nombre_modelo} ya está en tu carrito.', 'warning')
        return redirect(url_for('ver_carrito'))

    carrito.append(casco_id)
    session['carrito'] = carrito
    session.modified = True

    flash(f'{casco.marca} {casco.nombre_modelo} agregado al carrito.', 'success')
    return redirect(url_for('ver_carrito'))


@app.route('/carrito/quitar/<int:casco_id>', methods=['POST'])
def quitar_del_carrito(casco_id):
    carrito = session.get('carrito', [])
    if casco_id in carrito:
        carrito.remove(casco_id)
        session['carrito'] = carrito
        session.modified = True
        flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('ver_carrito'))


@app.route('/carrito')
def ver_carrito():
    carrito_ids = session.get('carrito', [])
    cascos = Casco.query.filter(Casco.id.in_(carrito_ids)).all() if carrito_ids else []
    total = sum(c.precio for c in cascos)
    return render_template('carrito.html', cascos=cascos, total=total)


# -------------------------------------------------------
# RUTAS CHECKOUT
# -------------------------------------------------------
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    carrito_ids = session.get('carrito', [])
    if not carrito_ids:
        flash('Tu carrito está vacío.', 'warning')
        return redirect(url_for('index'))

    cascos = Casco.query.filter(Casco.id.in_(carrito_ids)).all()
    total = sum(c.precio for c in cascos)

    if request.method == 'POST':
        # Guardar datos del formulario en session para usarlos en el pago
        session['checkout_data'] = {
            'nombre': request.form['nombre'],
            'apellido': request.form['apellido'],
            'dni': request.form['dni'],
            'telefono': request.form['telefono'],
            'email': request.form.get('email', ''),
            'tipo_entrega': request.form['tipo_entrega'],
            'codigo_postal': request.form.get('codigo_postal', ''),
            'provincia': request.form.get('provincia', ''),
            'ciudad': request.form.get('ciudad', ''),
            'direccion': request.form.get('direccion', ''),
        }
        return redirect(url_for('elegir_pago'))

    return render_template('checkout.html', cascos=cascos, total=total)


@app.route('/pago/elegir')
def elegir_pago():
    if not session.get('checkout_data'):
        return redirect(url_for('checkout'))

    carrito_ids = session.get('carrito', [])
    cascos = Casco.query.filter(Casco.id.in_(carrito_ids)).all()
    total = sum(c.precio for c in cascos)

    return render_template('pago_metodo.html', cascos=cascos, total=total)


# -------------------------------------------------------
# PAGO CON TRANSFERENCIA
# -------------------------------------------------------
@app.route('/pago/transferencia', methods=['POST'])
def pago_transferencia():
    if not session.get('checkout_data') or not session.get('carrito'):
        return redirect(url_for('index'))

    checkout_data = session['checkout_data']
    carrito_ids = session['carrito']
    cascos = Casco.query.filter(Casco.id.in_(carrito_ids)).all()
    total = sum(c.precio for c in cascos)

    # Crear pedido en BD
    pedido = Pedido(
        nombre=checkout_data['nombre'],
        apellido=checkout_data['apellido'],
        dni=checkout_data['dni'],
        telefono=checkout_data['telefono'],
        email=checkout_data.get('email', ''),
        tipo_entrega=checkout_data['tipo_entrega'],
        codigo_postal=checkout_data.get('codigo_postal', ''),
        provincia=checkout_data.get('provincia', ''),
        ciudad=checkout_data.get('ciudad', ''),
        direccion=checkout_data.get('direccion', ''),
        metodo_pago='transferencia',
        estado='pendiente',
        total=total
    )
    db.session.add(pedido)
    db.session.flush()  # Para obtener el ID antes del commit

    # Agregar items y marcar cascos como reservados
    for casco in cascos:
        item = ItemPedido(pedido_id=pedido.id, casco_id=casco.id, precio=casco.precio)
        db.session.add(item)
        casco.reservado = True

    db.session.commit()

    # Limpiar session
    session.pop('carrito', None)
    session.pop('checkout_data', None)

    # Datos de transferencia desde variables de entorno
    datos_transferencia = {
        'cbu': os.getenv('TRANSFERENCIA_CBU', ''),
        'alias': os.getenv('TRANSFERENCIA_ALIAS', ''),
        'titular': os.getenv('TRANSFERENCIA_TITULAR', ''),
        'cuil': os.getenv('TRANSFERENCIA_CUIL', ''),
    }

    # Armar mensaje WhatsApp
    items_texto = ', '.join([f"{c.marca} {c.nombre_modelo}" for c in cascos])
    entrega_texto = f"Envío a {checkout_data.get('ciudad', '')}, {checkout_data.get('provincia', '')}" if checkout_data['tipo_entrega'] == 'envio' else "Retiro en local"
    wsp_mensaje = (
        f"Hola! Realicé una transferencia para el pedido #{pedido.id}. "
        f"Productos: {items_texto}. "
        f"Entrega: {entrega_texto}. "
        f"Te envío el comprobante a continuación 📎"
    )
    wsp_numero = os.getenv('WSP_NUMERO', '5492954544001')
    wsp_url = f"https://wa.me/{wsp_numero}?text={wsp_mensaje}"

    return render_template('transferencia.html',
                           pedido=pedido,
                           cascos=cascos,
                           datos=datos_transferencia,
                           wsp_url=wsp_url)


# -------------------------------------------------------
# PAGO CON MERCADOPAGO
# -------------------------------------------------------
@app.route('/pago/mercadopago', methods=['POST'])
def pago_mercadopago():
    if not session.get('checkout_data') or not session.get('carrito'):
        return redirect(url_for('index'))

    try:
        import mercadopago
        sdk = mercadopago.SDK(os.getenv('MP_ACCESS_TOKEN'))

        checkout_data = session['checkout_data']
        carrito_ids = session['carrito']
        cascos = Casco.query.filter(Casco.id.in_(carrito_ids)).all()
        total = sum(c.precio for c in cascos)

        # Crear pedido pendiente en BD
        pedido = Pedido(
            nombre=checkout_data['nombre'],
            apellido=checkout_data['apellido'],
            dni=checkout_data['dni'],
            telefono=checkout_data['telefono'],
            email=checkout_data.get('email', ''),
            tipo_entrega=checkout_data['tipo_entrega'],
            codigo_postal=checkout_data.get('codigo_postal', ''),
            provincia=checkout_data.get('provincia', ''),
            ciudad=checkout_data.get('ciudad', ''),
            direccion=checkout_data.get('direccion', ''),
            metodo_pago='mercadopago',
            estado='pendiente',
            total=total
        )
        db.session.add(pedido)
        db.session.flush()

        for casco in cascos:
            item = ItemPedido(pedido_id=pedido.id, casco_id=casco.id, precio=casco.precio)
            db.session.add(item)
            casco.reservado = True

        db.session.commit()

        # Guardar pedido_id en session para las páginas de resultado
        session['pedido_id'] = pedido.id

        # Crear preferencia en MP
        items_mp = [{
            "title": f"{c.marca} {c.nombre_modelo}",
            "quantity": 1,
            "unit_price": float(c.precio),
            "currency_id": "ARS"
        } for c in cascos]

        base_url = os.getenv('BASE_URL', request.host_url.rstrip('/'))

        preference_data = {
            "items": items_mp,
            "payer": {
                "name": checkout_data['nombre'],
                "surname": checkout_data['apellido'],
                "email": checkout_data.get('email', 'cliente@whiphelmets.com'),
            },
            "back_urls": {
                "success": f"{base_url}/pago/exitoso",
                "failure": f"{base_url}/pago/fallido",
                "pending": f"{base_url}/pago/pendiente",
            },
            "auto_return": "approved",
            "external_reference": str(pedido.id),
        }

        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        # Limpiar carrito y checkout_data (el pedido ya está guardado)
        session.pop('carrito', None)
        session.pop('checkout_data', None)

        return redirect(preference["init_point"])

    except Exception as e:
        print(f"❌ Error MercadoPago: {e}")
        flash(f'Error al procesar el pago: {str(e)}', 'error')
        return redirect(url_for('elegir_pago'))


# -------------------------------------------------------
# RESULTADOS DE PAGO
# -------------------------------------------------------
@app.route('/pago/exitoso')
def pago_exitoso():
    pedido_id = request.args.get('external_reference') or session.get('pedido_id')
    pedido = Pedido.query.get(pedido_id) if pedido_id else None

    if pedido:
        pedido.mp_payment_id = request.args.get('payment_id', '')
        pedido.estado = 'confirmado'
        for item in pedido.items:
            item.casco.disponible = False
            item.casco.reservado = False
        db.session.commit()

    wsp_numero = os.getenv('WSP_NUMERO', '5492954544001')
    if pedido:
        items_texto = ', '.join([f"{i.casco.marca} {i.casco.nombre_modelo}" for i in pedido.items])
        entrega_texto = f"Envío a {pedido.ciudad}, {pedido.provincia}" if pedido.tipo_entrega == 'envio' else "Retiro en local"
        wsp_mensaje = (
            f"Hola! Acabo de realizar el pago del pedido #{pedido.id}. "
            f"Productos: {items_texto}. "
            f"Entrega: {entrega_texto}. "
            f"Quedo a la espera de coordinar 🙌"
        )
        wsp_url = f"https://wa.me/{wsp_numero}?text={wsp_mensaje}"
    else:
        wsp_url = f"https://wa.me/{wsp_numero}"

    return render_template('pago_exitoso.html', pedido=pedido, wsp_url=wsp_url)


@app.route('/pago/fallido')
def pago_fallido():
    pedido_id = request.args.get('external_reference') or session.get('pedido_id')
    pedido = Pedido.query.get(pedido_id) if pedido_id else None

    if pedido:
        pedido.estado = 'rechazado'
        for item in pedido.items:
            item.casco.reservado = False
        db.session.commit()

    wsp_numero = os.getenv('WSP_NUMERO', '5492954544001')
    if pedido:
        items_texto = ', '.join([f"{i.casco.marca} {i.casco.nombre_modelo}" for i in pedido.items])
        wsp_mensaje = (
            f"Hola! Tuve un problema al intentar pagar el pedido #{pedido.id}. "
            f"Productos: {items_texto}. "
            f"¿Me pueden ayudar a resolverlo?"
        )
        wsp_url = f"https://wa.me/{wsp_numero}?text={wsp_mensaje}"
    else:
        wsp_url = f"https://wa.me/{wsp_numero}"

    return render_template('pago_fallido.html', pedido=pedido, wsp_url=wsp_url)


@app.route('/pago/pendiente')
def pago_pendiente():
    pedido_id = request.args.get('external_reference') or session.get('pedido_id')
    pedido = Pedido.query.get(pedido_id) if pedido_id else None

    wsp_numero = os.getenv('WSP_NUMERO', '5492954544001')
    wsp_url = f"https://wa.me/{wsp_numero}"

    return render_template('pago_pendiente.html', pedido=pedido, wsp_url=wsp_url)


# -------------------------------------------------------
# ADMIN — PEDIDOS
# -------------------------------------------------------
@app.route('/admin/pedidos')
@login_required
def admin_pedidos():
    estado_filtro = request.args.get('estado', '')
    query = Pedido.query
    if estado_filtro:
        query = query.filter_by(estado=estado_filtro)
    pedidos = query.order_by(Pedido.fecha.desc()).all()
    return render_template('admin_pedidos.html', pedidos=pedidos, estado_filtro=estado_filtro)


@app.route('/admin/pedidos/<int:pedido_id>/confirmar', methods=['POST'])
@login_required
def confirmar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'confirmado'
    for item in pedido.items:
        item.casco.disponible = False
        item.casco.reservado = False
    db.session.commit()
    flash(f'Pedido #{pedido.id} confirmado. Cascos marcados como vendidos.', 'success')
    return redirect(url_for('admin_pedidos'))


@app.route('/admin/pedidos/<int:pedido_id>/rechazar', methods=['POST'])
@login_required
def rechazar_pedido(pedido_id):
    pedido = Pedido.query.get_or_404(pedido_id)
    pedido.estado = 'rechazado'
    for item in pedido.items:
        item.casco.reservado = False
    db.session.commit()
    flash(f'Pedido #{pedido.id} rechazado. Cascos disponibles nuevamente.', 'warning')
    return redirect(url_for('admin_pedidos'))


# -------------------------------------------------------
# RUTAS ADMIN EXISTENTES
# -------------------------------------------------------
@app.route('/admin/agregar', methods=['GET', 'POST'])
@login_required
def agregar_casco():
    if request.method == 'POST':
        aplicar_rembg = request.form.get('remover_fondo') == 'on'
        imagen_principal_url = ''

        if 'imagen_principal' in request.files:
            file = request.files['imagen_principal']
            if file.filename != '':
                try:
                    upload_result = subir_imagen(file, aplicar_rembg)
                    imagen_principal_url = upload_result['secure_url']
                except Exception as e:
                    flash(f'Error subiendo imagen: {str(e)}', 'error')
                    return redirect(url_for('agregar_casco'))

        imagenes_adicionales = []
        if 'imagenes_adicionales' in request.files:
            files = request.files.getlist('imagenes_adicionales')
            for file in files:
                if file.filename != '':
                    try:
                        upload_result = subir_imagen(file, aplicar_rembg)
                        imagenes_adicionales.append(upload_result['secure_url'])
                    except Exception as e:
                        print(f"❌ Error subiendo imagen adicional: {e}")

        nuevo_casco = Casco(
            nombre_modelo=request.form['nombre_modelo'],
            marca=request.form['marca'],
            tipo=request.form['tipo'],
            condicion=request.form['condicion'],
            precio=float(request.form['precio']),
            descripcion=request.form.get('descripcion', ''),
            talle=request.form.get('talle', ''),
            color=request.form.get('color', ''),
            imagen_principal=imagen_principal_url,
            imagenes_adicionales=','.join(imagenes_adicionales) if imagenes_adicionales else '',
            instagram_url=request.form.get('instagram_url', ''),
            disponible=True,
            destacado=request.form.get('destacado') == 'on'
        )

        db.session.add(nuevo_casco)
        db.session.commit()
        flash('Casco agregado exitosamente!', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('agregar_casco.html')


@app.route('/admin')
@login_required
def admin_panel():
    pagina = request.args.get('pagina', 1, type=int)
    orden = request.args.get('orden', 'fecha')
    direccion = request.args.get('dir', 'desc')

    columnas_validas = {
        'marca': Casco.marca,
        'modelo': Casco.nombre_modelo,
        'condicion': Casco.condicion,
        'precio': Casco.precio,
        'talle': Casco.talle,
        'disponible': Casco.disponible,
        'fecha': Casco.fecha_agregado
    }

    col = columnas_validas.get(orden, Casco.fecha_agregado)
    col = col.desc() if direccion == 'desc' else col.asc()

    cascos_paginados = Casco.query.order_by(col).paginate(
        page=pagina, per_page=7, error_out=False
    )

    return render_template('admin_panel.html',
                           cascos=cascos_paginados.items,
                           paginacion=cascos_paginados,
                           orden=orden,
                           direccion=direccion)


@app.route('/admin/editar/<int:casco_id>', methods=['GET', 'POST'])
@login_required
def editar_casco(casco_id):
    casco = Casco.query.get_or_404(casco_id)

    if request.method == 'POST':
        aplicar_rembg = request.form.get('remover_fondo') == 'on'

        if 'imagen_principal' in request.files:
            file = request.files['imagen_principal']
            if file.filename != '':
                try:
                    if casco.imagen_principal and '/upload/' in casco.imagen_principal:
                        after_upload = casco.imagen_principal.split('/upload/')[1]
                        if after_upload.startswith('v'):
                            after_upload = after_upload.split('/', 1)[1]
                        old_public_id = after_upload.rsplit('.', 1)[0]
                        cloudinary.uploader.destroy(old_public_id)
                    upload_result = subir_imagen(file, aplicar_rembg)
                    casco.imagen_principal = upload_result['secure_url']
                except Exception as e:
                    flash(f'Error subiendo imagen: {str(e)}', 'error')

        imagenes_adicionales = casco.imagenes_adicionales.split(',') if casco.imagenes_adicionales else []

        if 'imagenes_adicionales' in request.files:
            files = request.files.getlist('imagenes_adicionales')
            for file in files:
                if file.filename != '':
                    try:
                        upload_result = subir_imagen(file, aplicar_rembg)
                        imagenes_adicionales.append(upload_result['secure_url'])
                    except Exception as e:
                        print(f"❌ Error: {e}")

        casco.imagenes_adicionales = ','.join(imagenes_adicionales) if imagenes_adicionales else None
        casco.nombre_modelo = request.form['nombre_modelo']
        casco.marca = request.form['marca']
        casco.tipo = request.form.get('tipo', '')
        casco.condicion = request.form.get('condicion', 'nuevo')
        casco.precio = float(request.form['precio'])
        casco.descripcion = request.form.get('descripcion', '')
        casco.talle = request.form.get('talle', '')
        casco.color = request.form.get('color', '')
        casco.instagram_url = request.form.get('instagram_url', '')
        casco.disponible = 'disponible' in request.form
        casco.destacado = 'destacado' in request.form

        db.session.commit()
        flash('Casco actualizado correctamente', 'success')
        return redirect(url_for('admin_panel'))

    return render_template('editar_casco.html', casco=casco)


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin_user = os.getenv('ADMIN_USERNAME', 'admin')
        admin_pass = os.getenv('ADMIN_PASSWORD', 'admin')
        if username == admin_user and password == admin_pass:
            user = User(id=1)
            login_user(user)
            flash('¡Bienvenido!', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))


@app.route('/admin/eliminar-imagen/<int:casco_id>/<tipo>/<int:indice>', methods=['POST'])
@login_required
def eliminar_imagen(casco_id, tipo, indice):
    casco = Casco.query.get_or_404(casco_id)
    try:
        if tipo == 'principal':
            if casco.imagen_principal and '/upload/' in casco.imagen_principal:
                after_upload = casco.imagen_principal.split('/upload/')[1]
                if after_upload.startswith('v'):
                    after_upload = after_upload.split('/', 1)[1]
                public_id = after_upload.rsplit('.', 1)[0]
                cloudinary.uploader.destroy(public_id)
                casco.imagen_principal = None
                flash('Imagen principal eliminada', 'success')
        elif tipo == 'adicional':
            imagenes_raw = casco.imagenes_adicionales.split(',') if casco.imagenes_adicionales else []
            if not (0 <= indice < len(imagenes_raw)):
                flash('Índice inválido', 'error')
                return redirect(url_for('editar_casco', casco_id=casco_id))
            imagen_url = imagenes_raw[indice].strip()
            if not imagen_url:
                imagenes_raw.pop(indice)
                imagenes_limpias = [i for i in imagenes_raw if i.strip()]
                casco.imagenes_adicionales = ','.join(imagenes_limpias) if imagenes_limpias else None
                db.session.commit()
                flash('Slot vacío eliminado', 'success')
                return redirect(url_for('editar_casco', casco_id=casco_id))
            if '/upload/' in imagen_url:
                after_upload = imagen_url.split('/upload/')[1]
                if after_upload.startswith('v'):
                    after_upload = after_upload.split('/', 1)[1]
                public_id = after_upload.rsplit('.', 1)[0]
                cloudinary.uploader.destroy(public_id)
            imagenes_raw.pop(indice)
            imagenes_limpias = [i for i in imagenes_raw if i.strip()]
            casco.imagenes_adicionales = ','.join(imagenes_limpias) if imagenes_limpias else None
            flash('Imagen adicional eliminada', 'success')
        db.session.commit()
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    return redirect(url_for('editar_casco', casco_id=casco_id))


@app.route('/admin/eliminar-casco/<int:casco_id>', methods=['POST'])
@login_required
def eliminar_casco(casco_id):
    casco = Casco.query.get_or_404(casco_id)
    try:
        if casco.imagen_principal and '/upload/' in casco.imagen_principal:
            after_upload = casco.imagen_principal.split('/upload/')[1]
            if after_upload.startswith('v'):
                after_upload = after_upload.split('/', 1)[1]
            public_id = after_upload.rsplit('.', 1)[0]
            cloudinary.uploader.destroy(public_id)
        if casco.imagenes_adicionales:
            for img_url in casco.imagenes_adicionales.split(','):
                img_url = img_url.strip()
                if img_url and '/upload/' in img_url:
                    after_upload = img_url.split('/upload/')[1]
                    if after_upload.startswith('v'):
                        after_upload = after_upload.split('/', 1)[1]
                    public_id = after_upload.rsplit('.', 1)[0]
                    cloudinary.uploader.destroy(public_id)
        db.session.delete(casco)
        db.session.commit()
        flash(f'Casco "{casco.marca} {casco.nombre_modelo}" eliminado correctamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar: {str(e)}', 'error')
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
