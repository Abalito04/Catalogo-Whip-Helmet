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

# base.html
target_base = """                <div class="nav-links">
                    <a href="https://www.instagram.com/whip.helmets/" target="_blank" class="instagram-btn">"""
replace_base = """                <div class="nav-links">
                    <a href="{{ url_for('index', categoria='casco') }}" class="nav-link">
                        🏍️ Cascos
                    </a>
                    <a href="{{ url_for('index', categoria='indumentaria') }}" class="nav-link">
                        👕 Indumentaria
                    </a>
                    <a href="https://www.instagram.com/whip.helmets/" target="_blank" class="instagram-btn">"""
patch_file('templates/base.html', target_base, replace_base)

# index.html - part 1
target_index1 = """            <a href="{{ url_for('index', condicion='nuevo', tipo=filtro_actual.tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn {% if filtro_actual.condicion == 'nuevo' %}active{% endif %}">
                🟢 Nuevos
            </a>
            <a href="{{ url_for('index', condicion='usado', tipo=filtro_actual.tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn {% if filtro_actual.condicion == 'usado' %}active{% endif %}">
                🟡 Usados
            </a>
            <a href="{{ url_for('index', tipo=filtro_actual.tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn">"""
replace_index1 = """            <a href="{{ url_for('index', categoria=request.args.get('categoria'), condicion='nuevo', tipo=filtro_actual.tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn {% if filtro_actual.condicion == 'nuevo' %}active{% endif %}">
                🟢 Nuevos
            </a>
            <a href="{{ url_for('index', categoria=request.args.get('categoria'), condicion='usado', tipo=filtro_actual.tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn {% if filtro_actual.condicion == 'usado' %}active{% endif %}">
                🟡 Usados
            </a>
            <a href="{{ url_for('index', categoria=request.args.get('categoria'), tipo=filtro_actual.tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn">"""
patch_file('templates/index.html', target_index1, replace_index1)

# index.html - part 2
target_index2 = """            <a href="{{ url_for('index', condicion=filtro_actual.condicion, tipo=tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn {% if filtro_actual.tipo == tipo %}active{% endif %}">"""
replace_index2 = """            <a href="{{ url_for('index', categoria=request.args.get('categoria'), condicion=filtro_actual.condicion, tipo=tipo, marca=filtro_actual.marca) }}"
               class="filtro-btn {% if filtro_actual.tipo == tipo %}active{% endif %}">"""
patch_file('templates/index.html', target_index2, replace_index2)

# index.html - part 3
target_index3 = """            <a href="{{ url_for('index', condicion=filtro_actual.condicion, tipo=filtro_actual.tipo, marca=marca) }}"
               class="filtro-btn {% if filtro_actual.marca == marca %}active{% endif %}">"""
replace_index3 = """            <a href="{{ url_for('index', categoria=request.args.get('categoria'), condicion=filtro_actual.condicion, tipo=filtro_actual.tipo, marca=marca) }}"
               class="filtro-btn {% if filtro_actual.marca == marca %}active{% endif %}">"""
patch_file('templates/index.html', target_index3, replace_index3)

# index.html - part 4
target_index4 = """        {% if filtro_actual.condicion or filtro_actual.tipo or filtro_actual.marca %}
        <a href="{{ url_for('index') }}" class="limpiar-filtros">Limpiar filtros</a>
        {% endif %}"""
replace_index4 = """        {% if filtro_actual.condicion or filtro_actual.tipo or filtro_actual.marca or request.args.get('categoria') %}
        <a href="{{ url_for('index') }}" class="limpiar-filtros">Limpiar filtros</a>
        {% endif %}"""
patch_file('templates/index.html', target_index4, replace_index4)

