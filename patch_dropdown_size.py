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

t_css = """    .dropdown { order: 1; flex: 1 1 calc(50% - 10px); }
    .nav-secciones-btn { width: 100%; min-height: 40px; }"""

r_css = """    .dropdown { 
        order: 1; 
        flex: 1 1 calc(33% - 10px) !important;
    }
    .nav-secciones-btn { 
        width: 100%; 
        padding: 10px 16px !important;
        font-size: 13px !important;
        min-height: 40px;
        white-space: nowrap;
        display: flex;
        align-items: center;
        justify-content: center;
    }"""

patch_file('static/css/style.css', t_css, r_css)
