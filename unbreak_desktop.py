import glob

files = [
    "Restaurant_Portal_Dashboard.html",
    "Excess_Notification_Center.html",
    "Restaurant_Locations_Management.html",
    "Restaurant_Analytics_and_Impact.html",
    "Restaurant_Team_Management.html"
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove the display: flex !important; from the inline style we just injected
    content = content.replace("display: flex !important;", "display: flex;")
    
    # I should also add a media query to the head to properly hide this on desktop 
    # since we added a specific ID or class? No, lg:hidden has "display: none". If we have "display: flex;" inline, it might still override lg:hidden.
    
    # Let's completely remove "display: flex;" from inline style since it's already a flex container by default or handled by tailwind.
    content = content.replace("display: flex;", "")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Removed inline display style to prevent desktop overlap.")
