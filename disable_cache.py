import glob
import re

files = glob.glob("*.html")
meta_tags = """
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
"""

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Inject right after <head>
    if "<head>" in content and "must-revalidate" not in content:
        content = content.replace("<head>", f"<head>{meta_tags}")
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)

print("Injected no-cache meta tags into all HTML files.")
