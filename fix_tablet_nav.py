import glob
import re

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
    
    # Replace md:hidden with lg:hidden in the mobile bottom navigation
    content = content.replace(
        '<nav class="md:hidden fixed bottom-0',
        '<nav class="lg:hidden fixed bottom-0'
    )

    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Updated nav visibility to lg:hidden across all 5 pages.")
