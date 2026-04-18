import os
from bs4 import BeautifulSoup

files = [
    "Restaurant_Portal_Dashboard.html",
    "Restaurant_Locations_Management.html",
    "Restaurant_Team_Management.html",
    "Restaurant_Analytics_and_Impact.html",
    "Excess_Notification_Center.html"
]

navbar_html = """
<div class="fixed top-6 left-1/2 -translate-x-1/2 w-[95%] max-w-6xl z-50 flex justify-center">
    <header class="w-full flex justify-between items-center px-6 md:px-8 py-3.5 bg-white/95 dark:bg-[#121629]/95 backdrop-blur-xl border border-gray-200/80 dark:border-white/10 rounded-full shadow-[0_4px_20px_rgba(0,0,0,0.08)] dark:shadow-[0_8px_32px_rgba(0,0,0,0.3)] transition-all duration-300">
        <div class="flex items-center gap-3">
            <span class="material-symbols-outlined text-[#4a7c59] dark:text-indigo-400 text-3xl">soup_kitchen</span>
            <span class="text-xl font-bold font-['Literata'] text-gray-900 dark:text-white">AnnaSetu Portal</span>
        </div>
        <nav class="hidden lg:flex items-center gap-6">
            <a class="text-sm font-semibold text-gray-600 dark:text-gray-300 hover:text-[#4a7c59]" href="Restaurant_Portal_Dashboard.html">Dashboard</a>
            <a class="text-sm font-semibold text-gray-600 dark:text-gray-300 hover:text-[#4a7c59]" href="Excess_Notification_Center.html">Surplus Log</a>
            <a class="text-sm font-semibold text-gray-600 dark:text-gray-300 hover:text-[#4a7c59]" href="Restaurant_Locations_Management.html">Locations</a>
            <a class="text-sm font-semibold text-gray-600 dark:text-gray-300 hover:text-[#4a7c59]" href="Restaurant_Analytics_and_Impact.html">Analytics</a>
            <a class="text-sm font-semibold text-gray-600 dark:text-gray-300 hover:text-[#4a7c59]" href="Restaurant_Team_Management.html">Team</a>
            <a class="text-sm font-bold text-emerald-600 dark:text-emerald-400 hover:text-emerald-800" href="Impact_Hub.html">Impact Hub</a>
        </nav>
        <div class="flex items-center gap-4">
            <a href="index.html" class="hidden md:flex px-6 py-2.5 bg-red-500 text-white rounded-full font-bold text-sm tracking-wide hover:bg-red-600 transition-all">Logout</a>
            <button id="theme-toggle" class="w-10 h-10 rounded-full bg-gray-100 dark:bg-[#1e243b] flex items-center justify-center text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
                <span id="theme-icon" class="material-symbols-outlined text-lg">dark_mode</span>
            </button>
        </div>
    </header>
</div>
"""

script_html = """
<script>
    document.addEventListener("DOMContentLoaded", () => {
        const themeToggleBtn = document.getElementById('theme-toggle');
        const themeIcon = document.getElementById('theme-icon');
        const htmlElement = document.documentElement;

        if (themeToggleBtn) {
            themeToggleBtn.addEventListener('click', () => {
                htmlElement.classList.toggle('dark');
                htmlElement.classList.toggle('light');
                if (htmlElement.classList.contains('dark')) {
                    themeIcon.textContent = 'light_mode';
                    htmlElement.style.backgroundColor = '#111';
                } else {
                    themeIcon.textContent = 'dark_mode';
                    htmlElement.style.backgroundColor = '';
                }
            });
        }
    });
</script>
"""

dir_path = r"c:\Users\User\OneDrive\Desktop\AnnaSetu\AnnaSetu-ai-powered-food-rescue-network"

def transform_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # 1. Remove Sidebar
    aside = soup.find('aside')
    if aside:
        aside.decompose()
        
    # 2. Remove bottom nav (mobile)
    bottom_nav = soup.find('nav', class_=lambda c: c and 'fixed bottom-0' in c)
    if bottom_nav:
        bottom_nav.decompose()
        
    # 3. Replace old header with new navbar
    header = soup.find('header')
    if header:
        new_header = BeautifulSoup(navbar_html, 'html.parser')
        header.replace_with(new_header)
        
    # 4. Add top padding to main
    main = soup.find('main')
    if main:
        classes = main.get('class', [])
        # Append pt-32 to allow space for the floating navbar
        if 'pt-32' not in classes:
            classes.append('pt-32')
        main['class'] = classes
        
    # 5. Append scripts to body
    body = soup.find('body')
    if body:
        # Check if already added
        if not body.find('script', string=lambda s: s and 'themeToggleBtn' in s):
            new_script = BeautifulSoup(script_html, 'html.parser')
            body.append(new_script)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Transformed {filepath}")

for f in files:
    transform_file(os.path.join(dir_path, f))
