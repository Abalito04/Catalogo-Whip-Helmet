import sys

def patch_file(filepath, target, replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if target in content:
        content = content.replace(target, replacement)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"Target not found in {filepath}")

# agregar_casco.html - part 1
t_add1 = """<div class="container" style="max-width: 800px; margin: 50px auto;">
    <h1 style="color: #ffd700; margin-bottom: 30px;">Agregar Nuevo Casco</h1>"""
r_add1 = """<div class="container" style="max-width: 800px; margin: 50px auto;">
    <h1 style="color: #ffd700; margin-bottom: 30px;">Agregar Nuevo Producto</h1>"""
patch_file('templates/agregar_casco.html', t_add1, r_add1)

# agregar_casco.html - part 2
t_add2 = """        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Condición *</label>"""
r_add2 = """        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Categoría *</label>
            <select name="categoria" required
                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                <option value="casco">Casco</option>
                <option value="indumentaria">Indumentaria</option>
            </select>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Condición *</label>"""
patch_file('templates/agregar_casco.html', t_add2, r_add2)

# agregar_casco.html - part 3
t_add3 = """                Agregar Casco
            </button>"""
r_add3 = """                Agregar Producto
            </button>"""
patch_file('templates/agregar_casco.html', t_add3, r_add3)


# editar_casco.html - part 1
t_edit1 = """<div class="container" style="max-width: 800px; margin: 50px auto;">
    <h1 style="color: #ffd700; margin-bottom: 30px;">Editar Casco</h1>"""
r_edit1 = """<div class="container" style="max-width: 800px; margin: 50px auto;">
    <h1 style="color: #ffd700; margin-bottom: 30px;">Editar Producto</h1>"""
patch_file('templates/editar_casco.html', t_edit1, r_edit1)

# editar_casco.html - part 2
t_edit2 = """        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Condición *</label>"""
r_edit2 = """        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Categoría *</label>
            <select name="categoria" required
                style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                <option value="casco" {% if casco.categoria == 'casco' %}selected{% endif %}>Casco</option>
                <option value="indumentaria" {% if casco.categoria == 'indumentaria' %}selected{% endif %}>Indumentaria</option>
            </select>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; margin-bottom: 5px; font-weight: bold;">Condición *</label>"""
patch_file('templates/editar_casco.html', t_edit2, r_edit2)

# editar_casco.html - part 3
t_edit3 = """                Guardar Cambios
            </button>"""
r_edit3 = """                Guardar Cambios
            </button>"""
patch_file('templates/editar_casco.html', t_edit3, r_edit3)


