import glob
import re

files = [
    "Restaurant_Portal_Dashboard.html",
    "Excess_Notification_Center.html",
    "Restaurant_Locations_Management.html",
    "Restaurant_Analytics_and_Impact.html",
    "Restaurant_Team_Management.html"
]

infallible_style = "position: fixed !important; bottom: 0 !important; left: 0 !important; right: 0 !important; width: 100vw !important; z-index: 2147483647 !important; display: flex !important; justify-content: space-around !important; align-items: center !important; height: 64px !important; background-color: rgba(255, 255, 255, 0.98) !important; backdrop-filter: blur(20px) !important; -webkit-backdrop-filter: blur(20px) !important; border-top: 1px solid #e5e7eb !important; padding-bottom: env(safe-area-inset-bottom) !important;"

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Let's replace the <nav> definition forcefully.
    # The existing nav class contains: class="lg:hidden fixed bottom-0 left-0 right-0 ... pb-[env(safe-area-inset-bottom)]" style="z-index: 9999 !important;"
    
    # First, let's find the nav tag itself and replace it completely to make sure it's foolproof.
    pattern = r'<nav class="lg:hidden[^>]*" style="z-index: 9999 !important;">'
    new_nav_tag = f'<nav class="lg:hidden fixed bottom-0 left-0 right-0 w-full" style="{infallible_style}">'
    
    if re.search(pattern, content):
        content = re.sub(pattern, new_nav_tag, content)
    else:
        # Fallback if something was slightly different
        pattern_fallback = r'<nav class="(?:md|lg):hidden[^>]*>'
        content = re.sub(pattern_fallback, new_nav_tag, content)

    # Let's also do something very important: Let's make sure the body doesn't hide overflow
    # and has proper styling
    content = content.replace("<body class=\"", "<body id=\"annasetu-body\" class=\"")

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Infallible mobile nav injected.")
