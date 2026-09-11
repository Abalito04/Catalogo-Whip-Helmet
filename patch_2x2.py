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

t_css1 = """    .nav-links a {
        padding: 10px 16px !important;
        font-size: 13px !important;
        flex: 1 1 calc(33% - 10px) !important;"""

r_css1 = """    .nav-links a {
        padding: 10px 16px !important;
        font-size: 13px !important;
        flex: 1 1 calc(50% - 10px) !important;"""

patch_file('static/css/style.css', t_css1, r_css1)

t_css2 = """    .dropdown { 
        order: 1; 
        flex: 1 1 calc(33% - 10px) !important;
    }"""

r_css2 = """    .dropdown { 
        order: 1; 
        flex: 1 1 calc(50% - 10px) !important;
    }"""

patch_file('static/css/style.css', t_css2, r_css2)
