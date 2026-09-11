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

t_css = """@media (max-width: 768px) {
    /* Body */"""

r_css = """@media (max-width: 768px) {
    /* Portal Categorias */
    .categorias-titulo {
        font-size: 28px;
        margin-bottom: 25px;
    }
    
    .categorias-grid {
        gap: 20px;
    }
    
    .categoria-img-container {
        height: 200px;
    }

    /* Body */"""

patch_file('static/css/style.css', t_css, r_css)
