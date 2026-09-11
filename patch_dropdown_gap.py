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

t_css = """    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    margin-top: 10px;
}"""

r_css = """    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    /* Padding invisible para evitar que se cierre el hover */
    margin-top: 0;
}

.dropdown::after {
    content: '';
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    height: 15px; /* Cubre el espacio en blanco inferior */
}"""

patch_file('static/css/style.css', t_css, r_css)
