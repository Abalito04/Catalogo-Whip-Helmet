# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Casco
import os
import io
import cloudinary
import cloudinary.uploader
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc71d03d236850d52e73d76371be47576120b2d29b8f849f99f06fbc63bf284c'

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
# RUTAS
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


@app.route('/admin/agregar', methods=['GET', 'POST'])
@login_required
def agregar_casco():
    if request.method == 'POST':
        aplicar_rembg = request.form.get('remover_fondo') == 'on'
        imagen_principal_url = ''

        if 'imagen_principal' in request.files:
            file = request.files['imagen_principal']
            if file.filename != '':
                print(f"📸 Subiendo imagen principal: {file.filename}")
                try:
                    upload_result = subir_imagen(file, aplicar_rembg)
                    imagen_principal_url = upload_result['secure_url']
                    print(f"✅ Imagen principal subida: {imagen_principal_url}")
                except Exception as e:
                    print(f"❌ Error subiendo imagen principal: {e}")
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

        imagenes_adicionales_str = ','.join(imagenes_adicionales) if imagenes_adicionales else ''

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
            imagenes_adicionales=imagenes_adicionales_str,
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
    cascos = Casco.query.order_by(Casco.fecha_agregado.desc()).all()
    return render_template('admin_panel.html', cascos=cascos)


@app.route('/admin/editar/<int:casco_id>', methods=['GET', 'POST'])
@login_required
def editar_casco(casco_id):
    casco = Casco.query.get_or_404(casco_id)

    if request.method == 'POST':
        aplicar_rembg = request.form.get('remover_fondo') == 'on'

        if 'imagen_principal' in request.files:
            file = request.files['imagen_principal']
            if file.filename != '':
                print(f"📸 Subiendo nueva imagen principal...")
                try:
                    if casco.imagen_principal and '/upload/' in casco.imagen_principal:
                        after_upload = casco.imagen_principal.split('/upload/')[1]
                        if after_upload.startswith('v'):
                            after_upload = after_upload.split('/', 1)[1]
                        old_public_id = after_upload.rsplit('.', 1)[0]
                        cloudinary.uploader.destroy(old_public_id)

                    upload_result = subir_imagen(file, aplicar_rembg)
                    casco.imagen_principal = upload_result['secure_url']
                    print(f"✅ Nueva imagen principal: {casco.imagen_principal}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    flash(f'Error subiendo imagen: {str(e)}', 'error')

        imagenes_adicionales = casco.imagenes_adicionales.split(',') if casco.imagenes_adicionales else []

        if 'imagenes_adicionales' in request.files:
            files = request.files.getlist('imagenes_adicionales')
            for file in files:
                if file.filename != '':
                    print(f"📸 Subiendo imagen adicional: {file.filename}")
                    try:
                        upload_result = subir_imagen(file, aplicar_rembg)
                        imagenes_adicionales.append(upload_result['secure_url'])
                        print(f"✅ Imagen adicional subida")
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
                print(f"🗑️ Eliminando imagen principal: {public_id}")
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
                print(f"🗑️ Eliminando imagen adicional: {public_id}")
                cloudinary.uploader.destroy(public_id)

            imagenes_raw.pop(indice)
            imagenes_limpias = [i for i in imagenes_raw if i.strip()]
            casco.imagenes_adicionales = ','.join(imagenes_limpias) if imagenes_limpias else None
            flash('Imagen adicional eliminada', 'success')

        db.session.commit()

    except Exception as e:
        print(f"❌ Error eliminando imagen: {e}")
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
        print(f"❌ Error eliminando casco: {e}")
        flash(f'Error al eliminar: {str(e)}', 'error')

    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
