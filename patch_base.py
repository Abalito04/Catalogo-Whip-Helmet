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

t_base = """                <div class="nav-links">
                    <a href="{{ url_for('index', categoria='casco') }}" class="nav-cascos-btn">
                        Cascos
                    </a>
                    <a href="{{ url_for('index', categoria='indumentaria') }}" class="nav-indumentaria-btn">
                        Indumentaria
                    </a>"""

r_base = """                <div class="nav-links">
                    <div class="dropdown">
                        <button class="nav-secciones-btn dropbtn">Secciones ▾</button>
                        <div class="dropdown-content">
                            <a href="{{ url_for('index', categoria='casco') }}">Cascos</a>
                            <a href="{{ url_for('index', categoria='indumentaria') }}">Indumentaria</a>
                        </div>
                    </div>"""

patch_file('templates/base.html', t_base, r_base)
