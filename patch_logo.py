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

t_css = """.logo img {
    height: 150px;
    width: auto;
}"""

r_css = """.logo img {
    height: 150px;
    width: 150px;
    border-radius: 50%;
    object-fit: cover;
}"""

patch_file('static/css/style.css', t_css, r_css)
