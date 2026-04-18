import os
import re

files = [
    "Restaurant_Portal_Dashboard.html",
    "Restaurant_Locations_Management.html",
    "Restaurant_Team_Management.html",
    "Restaurant_Analytics_and_Impact.html",
    "Excess_Notification_Center.html"
]

mapping = {
    "Dashboard": "Restaurant_Portal_Dashboard.html",
    "Surplus Log": "Excess_Notification_Center.html",
    "Locations": "Restaurant_Locations_Management.html",
    "Analytics": "Restaurant_Analytics_and_Impact.html",
    "Team": "Restaurant_Team_Management.html"
}

dir_path = r"c:\Users\User\OneDrive\Desktop\AnnaSetu\AnnaSetu-ai-powered-food-rescue-network"

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The HTML has specific spans for text like:
    # <span class="font-medium">Dashboard</span>
    # <a ... href="..."> ... <span class="font-medium">Dashboard</span></a> 
    
    # Let's do a regex replacement for each link.
    # We find the <a> block that contains the specific text.
    # We can do this safely using regex by targeting the exact text.
    for text, filename in mapping.items():
        # Match <a ... href="#" ... > ... <span class="font-medium">Text</span> ... </a>
        # Because we don't want to break the structure, we can just replace 'href="#"' with 'href="filename"'
        # ONLY IN the context of that specific <a> tag.
        
        # We can find all <a...>...</a>
        # and if it contains `>Text<`, we replace its first href="#" with href="filename".
        
        pattern = r'(<a[^>]*href=")([^"]*)("[^>]*>(?:(?!</a>).)*>'+text+'<)'
        # wait, regex might be tricky if the text is inside nested tags with newlines.
        
        pass

    # A simpler approach: use BeautifulSoup
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        navs = soup.find_all('nav')
        for nav in navs:
            for a in nav.find_all('a'):
                a_text = a.get_text(separator=' ', strip=True)
                for key, target_html in mapping.items():
                    if key in a_text:
                        a['href'] = target_html
                        break
        new_content = str(soup)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    except Exception as e:
        print(f"Error on {filepath}: {e}")

for f in files:
    update_file(os.path.join(dir_path, f))
