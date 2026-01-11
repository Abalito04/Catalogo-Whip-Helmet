# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Casco
import os
import cloudinary
import cloudinary.uploader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc71d03d236850d52e73d76371be47576120b2d29b8f849f99f06fbc63bf284c'

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
def agregar_casco():
    """Formulario para agregar cascos"""
    if request.method == 'POST':
        # Subir imagen a Cloudinary si existe
        imagen_url = ''
        if 'imagen' in request.files:
            file = request.files['imagen']
            if file.filename != '':
                upload_result = cloudinary.uploader.upload(
                    file,
                    folder="whip-helmets"
                )
                imagen_url = upload_result['secure_url']
        
        nuevo_casco = Casco(
            nombre_modelo=request.form['nombre_modelo'],
            marca=request.form['marca'],
            tipo=request.form['tipo'],
            condicion=request.form['condicion'],
            precio=float(request.form['precio']),
            descripcion=request.form.get('descripcion', ''),
            talle=request.form.get('talle', ''),
            color=request.form.get('color', ''),
            imagen_principal=imagen_url,
            disponible=True,
            destacado=request.form.get('destacado') == 'on'
        )
        
        db.session.add(nuevo_casco)
        db.session.commit()
        flash('Casco agregado exitosamente!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('agregar_casco.html')


@app.route('/admin')
def admin_panel():
    """Panel de administración"""
    cascos = Casco.query.order_by(Casco.fecha_agregado.desc()).all()
    return render_template('admin_panel.html', cascos=cascos)

@app.route('/admin/editar/<int:id>', methods=['GET', 'POST'])
def editar_casco(id):
    """Editar un casco existente"""
    casco = Casco.query.get_or_404(id)
    
    if request.method == 'POST':
        casco.nombre_modelo = request.form['nombre_modelo']
        casco.marca = request.form['marca']
        casco.tipo = request.form.get('tipo', '')
        casco.condicion = request.form['condicion']
        casco.precio = float(request.form['precio'])
        casco.descripcion = request.form.get('descripcion', '')
        casco.talle = request.form.get('talle', '')
        casco.color = request.form.get('color', '')
        casco.imagen_principal = request.form.get('imagen_principal', '')
        casco.disponible = request.form.get('disponible') == 'on'
        casco.destacado = request.form.get('destacado') == 'on'
        
        db.session.commit()
        flash('Casco actualizado exitosamente!', 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('editar_casco.html', casco=casco)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

