# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Casco
import os
import cloudinary
import cloudinary.uploader
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc71d03d236850d52e73d76371be47576120b2d29b8f849f99f06fbc63bf284c'

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Necesitás iniciar sesión para acceder.'

# Usuario simple (sin base de datos)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# Configurar Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# Railway usa postgres:// pero SQLAlchemy necesita postgresql://
database_url = os.getenv('DATABASE_URL', 'sqlite:///cascos.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializar base de datos
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Página principal - Catálogo completo"""
    # Obtener filtros de la URL
    condicion_filtro = request.args.get('condicion')
    tipo_filtro = request.args.get('tipo')
    marca_filtro = request.args.get('marca')
    
    # Query base
    query = Casco.query.filter_by(disponible=True)
    
    # Aplicar filtros
    if condicion_filtro:
        query = query.filter_by(condicion=condicion_filtro)
    if tipo_filtro:
        query = query.filter_by(tipo=tipo_filtro)
    if marca_filtro:
        query = query.filter_by(marca=marca_filtro)
    
    # Ordenar: destacados primero, luego por fecha
    cascos = query.order_by(Casco.destacado.desc(), Casco.fecha_agregado.desc()).all()
    
    # Obtener valores únicos para filtros
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
    """Vista individual del producto"""
    casco = Casco.query.get_or_404(id)
    return render_template('producto.html', casco=casco)

@app.route('/admin/agregar', methods=['GET', 'POST'])
@login_required
def agregar_casco():
    """Formulario para agregar cascos"""
    if request.method == 'POST':
        # Subir imagen principal
        imagen_principal_url = ''
        if 'imagen_principal' in request.files:
            file = request.files['imagen_principal']
            if file.filename != '':
                print(f"📸 Subiendo imagen principal: {file.filename}")  # Debug
                try:
                    upload_result = cloudinary.uploader.upload(
                        file,
                        folder="whip-helmets",
                        timeout=60  # Timeout de 60 segundos
                    )
                    imagen_principal_url = upload_result['secure_url']
                    print(f"✅ Imagen principal subida: {imagen_principal_url}")  # Debug
                except Exception as e:
                    print(f"❌ Error subiendo imagen principal: {e}")  # Debug
                    flash(f'Error subiendo imagen: {str(e)}', 'error')
                    return redirect(url_for('agregar_casco'))
                
        
        # Subir imágenes adicionales
        imagenes_adicionales = []
        if 'imagenes_adicionales' in request.files:
            files = request.files.getlist('imagenes_adicionales')
            for file in files:
                if file.filename != '':
                    upload_result = cloudinary.uploader.upload(
                        file,
                        folder="whip-helmets"
                    )
                    imagenes_adicionales.append(upload_result['secure_url'])
        
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
    """Panel de administración"""
    cascos = Casco.query.order_by(Casco.fecha_agregado.desc()).all()
    return render_template('admin_panel.html', cascos=cascos)

@app.route('/admin/editar/<int:casco_id>', methods=['GET', 'POST'])
@login_required
def editar_casco(casco_id):
    """Editar un casco existente"""
    casco = Casco.query.get_or_404(casco_id)
    
    if request.method == 'POST':
        # Actualizar imagen principal SOLO si se sube una nueva
        if 'imagen_principal' in request.files:
            file = request.files['imagen_principal']
            if file.filename != '':
                print(f"📸 Subiendo nueva imagen principal...")
                try:
                    # Eliminar la anterior de Cloudinary
                    if casco.imagen_principal_url:
                        old_public_id = casco.imagen_principal_url.split('/')[-1].split('.')[0]
                        cloudinary.uploader.destroy(f"whip-helmets/{old_public_id}")
                    
                    # Subir nueva
                    upload_result = cloudinary.uploader.upload(file, folder="whip-helmets", timeout=60)
                    casco.imagen_principal_url = upload_result['secure_url']
                    print(f"✅ Nueva imagen principal: {casco.imagen_principal_url}")
                except Exception as e:
                    print(f"❌ Error: {e}")
                    flash(f'Error subiendo imagen: {str(e)}', 'error')
        
        # AGREGAR imágenes adicionales (no reemplazar)
        imagenes_adicionales = casco.imagenes_adicionales_url.split(',') if casco.imagenes_adicionales_url else []
        
        if 'imagenes_adicionales' in request.files:
            files = request.files.getlist('imagenes_adicionales')
            for file in files:
                if file.filename != '':
                    print(f"📸 Subiendo imagen adicional: {file.filename}")
                    try:
                        upload_result = cloudinary.uploader.upload(file, folder="whip-helmets", timeout=60)
                        imagenes_adicionales.append(upload_result['secure_url'])
                        print(f"✅ Imagen adicional subida")
                    except Exception as e:
                        print(f"❌ Error: {e}")
        
        casco.imagenes_adicionales_url = ','.join(imagenes_adicionales) if imagenes_adicionales else None
        
        # Actualizar resto de campos
        casco.nombre = request.form['nombre']
        casco.marca = request.form['marca']
        casco.precio = float(request.form['precio'])
        casco.descripcion = request.form.get('descripcion', '')
        casco.instagram_url = request.form.get('instagram_url', '')
        casco.disponible = 'disponible' in request.form
        
        db.session.commit()
        flash('Casco actualizado correctamente', 'success')
        return redirect(url_for('admin'))
    
    return render_template('editar_casco.html', casco=casco)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login de admin"""
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
    """Cerrar sesión"""
    logout_user()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('index'))

@app.route('/admin/eliminar-imagen/<int:casco_id>/<tipo>/<int:indice>', methods=['POST'])
@login_required
def eliminar_imagen(casco_id, tipo, indice):
    """Eliminar una imagen específica de un casco"""
    casco = Casco.query.get_or_404(casco_id)
    
    try:
        if tipo == 'principal':
            # Eliminar de Cloudinary
            if casco.imagen_principal_url:
                public_id = casco.imagen_principal_url.split('/')[-1].split('.')[0]
                cloudinary.uploader.destroy(f"whip-helmets/{public_id}")
            casco.imagen_principal_url = None
            flash('Imagen principal eliminada', 'success')
            
        elif tipo == 'adicional':
            imagenes = casco.imagenes_adicionales_url.split(',') if casco.imagenes_adicionales_url else []
            if 0 <= indice < len(imagenes):
                # Eliminar de Cloudinary
                imagen_url = imagenes[indice]
                public_id = imagen_url.split('/')[-1].split('.')[0]
                cloudinary.uploader.destroy(f"whip-helmets/{public_id}")
                # Eliminar de la lista
                imagenes.pop(indice)
                casco.imagenes_adicionales_url = ','.join(imagenes) if imagenes else None
                flash('Imagen adicional eliminada', 'success')
        
        db.session.commit()
        
    except Exception as e:
        print(f"❌ Error eliminando imagen: {e}")
        flash(f'Error eliminando imagen: {str(e)}', 'error')
    
    return redirect(url_for('editar_casco', casco_id=casco_id))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

