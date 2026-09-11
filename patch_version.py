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

patch_file('templates/base.html', 'css/style.css\') }}?v=4', 'css/style.css\') }}?v=5')
patch_file('templates/base.html', 'css/style.css\') }}?v=3', 'css/style.css\') }}?v=5')
patch_file('templates/base.html', 'css/style.css\') }}?v=2', 'css/style.css\') }}?v=5')
patch_file('templates/base.html', 'css/style.css\') }}">', 'css/style.css\') }}?v=5">')
