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

t_css = """.navbar.scrolled .logo img {
    height: 80px;
    transition: height 0.3s ease;
}"""

r_css = """.navbar.scrolled .logo img {
    height: 80px;
    width: 80px;
    transition: height 0.3s ease, width 0.3s ease;
}"""

patch_file('static/css/style.css', t_css, r_css)
