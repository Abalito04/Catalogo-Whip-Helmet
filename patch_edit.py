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

# editar_casco.html - part 1
t_edit1 = """<div class="container" style="max-width: 900px; background: white; border-radius: 8px; padding: 30px; margin-top: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
    <h2 style="color: #333; margin-bottom: 30px;">Editar Casco</h2>"""
r_edit1 = """<div class="container" style="max-width: 900px; background: white; border-radius: 8px; padding: 30px; margin-top: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
    <h2 style="color: #333; margin-bottom: 30px;">Editar Producto</h2>"""
patch_file('templates/editar_casco.html', t_edit1, r_edit1)

# editar_casco.html - part 2
t_edit2 = """        <div style="margin-bottom: 20px;">
            <label style="display: block; font-weight: 600; color: #333; margin-bottom: 8px;">Condición *</label>"""
r_edit2 = """        <div style="margin-bottom: 20px;">
            <label style="display: block; font-weight: 600; color: #333; margin-bottom: 8px;">Categoría *</label>
            <select name="categoria" required style="width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 15px; box-sizing: border-box;">
                <option value="casco" {% if casco.categoria == 'casco' %}selected{% endif %}>Casco</option>
                <option value="indumentaria" {% if casco.categoria == 'indumentaria' %}selected{% endif %}>Indumentaria</option>
            </select>
        </div>

        <div style="margin-bottom: 20px;">
            <label style="display: block; font-weight: 600; color: #333; margin-bottom: 8px;">Condición *</label>"""
patch_file('templates/editar_casco.html', t_edit2, r_edit2)

