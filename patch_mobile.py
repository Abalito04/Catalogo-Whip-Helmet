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

t_mobile = """    .nav-links {
        width: 100%;
        justify-content: center;
        gap: 10px;
    }"""

r_mobile = """    .nav-links {
        width: 100%;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
    }"""

patch_file('static/css/style.css', t_mobile, r_mobile)
