import os
from bs4 import BeautifulSoup
import re

files = [
    "Restaurant_Portal_Dashboard.html",
    "Restaurant_Locations_Management.html",
    "Restaurant_Team_Management.html",
    "Restaurant_Analytics_and_Impact.html",
    "Excess_Notification_Center.html"
]

dir_path = r"c:\Users\User\OneDrive\Desktop\AnnaSetu\AnnaSetu-ai-powered-food-rescue-network"

def refine_navbar(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Remove Impact Hub link
    html = re.sub(r'<a[^>]*href="Impact_Hub\.html"[^>]*>.*?</a>', '', html)
    
    # 2. Change navbar link hover logic
    html = html.replace('hover:text-[#4a7c59]', 'hover:text-[#facc15] hover:-translate-y-0.5 transition-all duration-300')
    
    # 3. Change Logout button styling.
    # Current styling is: bg-red-500 text-white rounded-full font-bold text-sm tracking-wide hover:bg-red-600 transition-all
    # Replace with yellow styling: bg-[#facc15] text-[#1e1b4b] rounded-full font-bold text-sm tracking-wide hover:bg-[#fef08a] transition-all shadow-[0_0_15px_rgba(250,204,21,0.2)]
    
    # The safest way is to find the Logout button and replace its classes.
    soup = BeautifulSoup(html, 'html.parser')
    logout_btns = soup.find_all('a', string=re.compile('Logout', re.I))
    for btn in logout_btns:
        btn['class'] = "hidden md:flex px-6 py-2.5 bg-[#facc15] text-[#1e1b4b] rounded-full font-bold text-sm tracking-wide hover:bg-[#fef08a] transition-all duration-300 shadow-[0_0_15px_rgba(250,204,21,0.2)] hover:scale-105"
        
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Refined {filepath}")

for f in files:
    refine_navbar(os.path.join(dir_path, f))
