import json
import urllib.request
import os

with open(r'C:\Users\User\.gemini\antigravity\brain\43d2a515-5e28-47eb-b8b3-fb1e1e5db213\.system_generated\steps\21\output.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    if text.startswith('1: '):
        text = text[3:]
    data = json.loads(text)

os.chdir(r'c:\Users\User\OneDrive\Desktop\AnnaSetu\AnnaSetu-ai-powered-food-rescue-network')
for screen in data['screens']:
    title = screen['title'].replace(' ', '_').replace('&', 'and') + '.html'
    url = screen['htmlCode']['downloadUrl']
    print(f"Downloading {title}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        html = response.read()
        with open(title, 'wb') as out_f:
            out_f.write(html)
