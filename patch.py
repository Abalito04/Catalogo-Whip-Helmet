import sys
content = open('app.py', 'r', encoding='utf-8').read()

target1 = """        db.session.execute(db.text('ALTER TABLE cascos ADD COLUMN IF NOT EXISTS precio_3_cuotas FLOAT'))
        db.session.execute(db.text(\"ALTER TABLE pedidos ALTER COLUMN metodo_pago TYPE VARCHAR(30)\"))  # ← acá"""

replace1 = """        db.session.execute(db.text('ALTER TABLE cascos ADD COLUMN IF NOT EXISTS precio_3_cuotas FLOAT'))
        db.session.execute(db.text(\"ALTER TABLE cascos ADD COLUMN IF NOT EXISTS categoria VARCHAR(30) DEFAULT 'casco'\"))
        db.session.execute(db.text(\"ALTER TABLE pedidos ALTER COLUMN metodo_pago TYPE VARCHAR(30)\"))  # ← acá"""

if target1 in content:
    content = content.replace(target1, replace1)
    print("Patched 1!")

target2 = """    condicion_filtro = request.args.get('condicion')
    tipo_filtro = request.args.get('tipo')
    marca_filtro = request.args.get('marca')

    query = Casco.query.filter_by(disponible=True)

    if condicion_filtro:"""

replace2 = """    condicion_filtro = request.args.get('condicion')
    tipo_filtro = request.args.get('tipo')
    marca_filtro = request.args.get('marca')
    categoria_filtro = request.args.get('categoria')

    query = Casco.query.filter_by(disponible=True)

    if categoria_filtro:
        query = query.filter_by(categoria=categoria_filtro)
    if condicion_filtro:"""

if target2 in content:
    content = content.replace(target2, replace2)
    print("Patched 2!")

target3 = """            nombre_modelo=request.form['nombre_modelo'],
            marca=request.form['marca'],
            tipo=request.form['tipo'],
            condicion=request.form['condicion'],"""

replace3 = """            nombre_modelo=request.form['nombre_modelo'],
            marca=request.form['marca'],
            tipo=request.form['tipo'],
            categoria=request.form.get('categoria', 'casco'),
            condicion=request.form['condicion'],"""

if target3 in content:
    content = content.replace(target3, replace3)
    print("Patched 3!")

target4 = """        casco.nombre_modelo = request.form['nombre_modelo']
        casco.marca = request.form['marca']
        casco.tipo = request.form.get('tipo', '')
        casco.condicion = request.form.get('condicion', 'nuevo')"""

replace4 = """        casco.nombre_modelo = request.form['nombre_modelo']
        casco.marca = request.form['marca']
        casco.tipo = request.form.get('tipo', '')
        casco.categoria = request.form.get('categoria', 'casco')
        casco.condicion = request.form.get('condicion', 'nuevo')"""

if target4 in content:
    content = content.replace(target4, replace4)
    print("Patched 4!")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved!")
