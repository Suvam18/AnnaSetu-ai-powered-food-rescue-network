import os
from bs4 import BeautifulSoup

files = [
    "Restaurant_Portal_Dashboard.html",
    "Restaurant_Locations_Management.html",
    "Restaurant_Team_Management.html",
    "Restaurant_Analytics_and_Impact.html",
    "Excess_Notification_Center.html"
]

dir_path = r"c:\Users\User\OneDrive\Desktop\AnnaSetu\AnnaSetu-ai-powered-food-rescue-network"

def fix_main_alignment(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    main = soup.find('main')
    if main:
        classes = main.get('class', [])
        # Remove any sidebar-related left margin/padding classes
        to_remove = ['ml-64', 'ml-60', 'ml-72', 'overflow-y-auto', 'flex-1', 'min-h-screen']
        classes = [c for c in classes if c not in to_remove]
        # Set clean centred layout classes
        clean_classes = [
            'w-full', 'max-w-6xl', 'mx-auto',
            'px-6', 'py-10', 'md:px-10', 'md:py-14'
        ]
        # Merge without duplicates
        for c in clean_classes:
            if c not in classes:
                classes.append(c)
        main['class'] = classes

    # Also remove any leftover outer flex wrappers that may push content
    for div in soup.find_all('div'):
        cls = div.get('class', [])
        if 'flex' in cls and 'min-h-screen' in cls:
            div['class'] = ['w-full']
        if 'flex-1' in cls and 'flex' in cls and 'flex-col' in cls and 'min-w-0' in cls:
            div['class'] = ['w-full']

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Fixed: {os.path.basename(filepath)}")

for f in files:
    fix_main_alignment(os.path.join(dir_path, f))

print("\nAll pages are now properly centred.")
