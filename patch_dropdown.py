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

t_css = """.nav-cascos-btn, .nav-indumentaria-btn {
    background: #ffd700;
    color: #000 !important;
    text-decoration: none;
    padding: 14px 28px;
    border-radius: 8px;
    transition: all 0.3s;
    font-weight: 700 !important;
    font-size: 16px;
    box-shadow: 0 3px 10px rgba(255, 215, 0, 0.4);
}

.nav-cascos-btn:hover, .nav-indumentaria-btn:hover {
    background: #ffcc00 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(255, 215, 0, 0.6);
}"""

r_css = """/* Dropdown Menu */
.dropdown {
    position: relative;
    display: inline-block;
}

.nav-secciones-btn {
    background: #ffd700;
    color: #000 !important;
    text-decoration: none;
    padding: 14px 28px;
    border-radius: 8px;
    transition: all 0.3s;
    font-weight: 700 !important;
    font-size: 16px;
    border: none;
    cursor: pointer;
    box-shadow: 0 3px 10px rgba(255, 215, 0, 0.4);
    font-family: inherit;
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-secciones-btn:hover, .dropdown:hover .nav-secciones-btn {
    background: #ffcc00 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 15px rgba(255, 215, 0, 0.6);
}

.dropdown-content {
    display: none;
    position: absolute;
    background-color: #2a2a2a;
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.8);
    z-index: 1000;
    border-radius: 8px;
    overflow: hidden;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 10px;
}

.dropdown-content a {
    color: #ddd !important;
    padding: 12px 16px !important;
    text-decoration: none;
    display: block !important;
    text-align: left;
    font-weight: 500 !important;
    font-size: 15px !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

.dropdown-content a:hover {
    background-color: #ffd700 !important;
    color: #000 !important;
    transform: none !important;
}

.dropdown:hover .dropdown-content {
    display: block;
}"""

patch_file('static/css/style.css', t_css, r_css)

t_css2 = """    .nav-cascos-btn { order: 1; }
    .nav-indumentaria-btn { order: 2; }
    .nav-carrito { order: 3; }"""

r_css2 = """    .dropdown { order: 1; flex: 1 1 calc(50% - 10px); }
    .nav-secciones-btn { width: 100%; min-height: 40px; }
    .nav-carrito { order: 2; }"""

patch_file('static/css/style.css', t_css2, r_css2)
