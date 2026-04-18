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

def fix_layout(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Fix 1: Increase top padding on <body> to push all content below navbar
    # Add padding-top to body
    body = soup.find('body')
    if body:
        existing = body.get('style', '')
        body['style'] = existing + ' padding-top: 7rem;'

    # Fix 2: Fix the outer wrapper divs — remove flex layout that right-aligns content
    # The outer div has class "flex min-h-screen"
    outer_div = soup.find('div', class_=lambda c: c and 'flex' in c and 'min-h-screen' in c)
    if outer_div:
        outer_div['class'] = ['min-h-screen', 'w-full']

    # Fix 3: Fix the inner flex wrapper that wraps main content
    inner_wrapper = soup.find('div', class_=lambda c: c and 'flex-1' in c and 'flex' in c and 'flex-col' in c and 'min-w-0' in c)
    if inner_wrapper:
        inner_wrapper['class'] = ['w-full']

    # Fix 4: Fix main — ensure proper centering and padding
    main = soup.find('main')
    if main:
        classes = main.get('class', [])
        # Remove old pt-32 if present (body now handles it)
        if 'pt-32' in classes:
            classes.remove('pt-32')
        # Remove any overflow-y-auto that might clip
        if 'overflow-y-auto' in classes:
            classes.remove('overflow-y-auto')
        # Ensure centering classes
        for cls in ['max-w-7xl', 'mx-auto', 'w-full', 'px-6', 'py-10', 'md:px-10', 'md:py-12']:
            if cls not in classes:
                classes.append(cls)
        main['class'] = classes

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Fixed layout: {os.path.basename(filepath)}")

for f in files:
    fix_layout(os.path.join(dir_path, f))

print("\nDone! All pages are now centred and pushed below the navbar.")
