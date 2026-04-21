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
    
    # Let's cleanly set exactly what we want the nav tag to be
    # We find the nav tag we just placed
    old_prefix = '<nav class="lg:hidden fixed bottom-0 left-0 right-0 w-full"'
    new_prefix = '<nav class="lg:hidden fixed bottom-0 left-0 right-0 w-full flex justify-around items-center flex-row"'
    content = content.replace(old_prefix, new_prefix)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Restored flex classes to the nav tags.")
