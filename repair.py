import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace when eco is followed by an AnnaSetu span
    new_content = re.sub(r'(<span class="material-symbols-outlined[^>]*>)eco(</span>\s*<span[^>]*>AnnaSetu)', r'\g<1>soup_kitchen\g<2>', content)
    
    # Replace when eco is followed immediately by AnnaSetu text (like in footer)
    new_content = re.sub(r'(<span class="material-symbols-outlined[^>]*>)eco(</span>\s*AnnaSetu)', r'\g<1>soup_kitchen\g<2>', new_content)
    
    if new_content != content:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f'Updated {f}')
