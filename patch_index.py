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

t_html = """{% block content %}
<div class="catalogo-wrapper">
    <!-- Sidebar de Filtros -->"""

r_html = """{% block content %}

{% if not request.args.get('categoria') %}
<div class="categorias-iniciales">
    <h2 class="categorias-titulo">¿Qué estás buscando?</h2>
    <div class="categorias-grid">
        <a href="{{ url_for('index', categoria='casco') }}" class="categoria-card">
            <div class="categoria-img-container">
                <img src="{{ url_for('static', filename='images/cat-cascos.jpg') }}" alt="Cascos" onerror="this.src='https://placehold.co/600x400/2a2a2a/ffd700?text=Cascos'">
            </div>
            <h3>Cascos</h3>
        </a>
        <a href="{{ url_for('index', categoria='indumentaria') }}" class="categoria-card">
            <div class="categoria-img-container">
                <img src="{{ url_for('static', filename='images/cat-indumentaria.jpg') }}" alt="Indumentaria" onerror="this.src='https://placehold.co/600x400/2a2a2a/ffd700?text=Indumentaria'">
            </div>
            <h3>Indumentaria</h3>
        </a>
    </div>
</div>
{% else %}

<div class="catalogo-wrapper">
    <!-- Sidebar de Filtros -->"""

patch_file('templates/index.html', t_html, r_html)

t_html_end = """    </section>
</div>
{% endblock %}"""

r_html_end = """    </section>
</div>
{% endif %}
{% endblock %}"""

patch_file('templates/index.html', t_html_end, r_html_end)
