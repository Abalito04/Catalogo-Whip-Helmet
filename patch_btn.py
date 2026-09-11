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
                    <a href="{{ url_for('index', categoria='casco') }}" class="nav-link">
                        🏍️ Cascos
                    </a>
                    <a href="{{ url_for('index', categoria='indumentaria') }}" class="nav-link">
                        👕 Indumentaria
                    </a>
                    <a href="https://www.instagram.com/whip.helmets/" target="_blank" class="instagram-btn">"""

r_base = """                <div class="nav-links">
                    <a href="{{ url_for('index', categoria='casco') }}" class="nav-cascos-btn">
                        🏍️ Cascos
                    </a>
                    <a href="{{ url_for('index', categoria='indumentaria') }}" class="nav-indumentaria-btn">
                        👕 Indumentaria
                    </a>
                    <a href="https://www.instagram.com/whip.helmets/" target="_blank" class="instagram-btn">"""

patch_file('templates/base.html', t_base, r_base)

t_css = """/* Versión autenticado */
.admin-btn.authenticated {
    background: #ffd700;
    color: #000;
}"""

r_css = """/* Versión autenticado */
.admin-btn.authenticated {
    background: #ffd700;
    color: #000;
}

.nav-cascos-btn {
    background: #dc3545;
    color: white;
    box-shadow: 0 3px 10px rgba(220, 53, 69, 0.4);
}
.nav-cascos-btn:hover {
    background: #c82333;
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(220, 53, 69, 0.6);
}

.nav-indumentaria-btn {
    background: #007bff;
    color: white;
    box-shadow: 0 3px 10px rgba(0, 123, 255, 0.4);
}
.nav-indumentaria-btn:hover {
    background: #0056b3;
    transform: translateY(-3px);
    box-shadow: 0 6px 15px rgba(0, 123, 255, 0.6);
}"""

patch_file('static/css/style.css', t_css, r_css)
