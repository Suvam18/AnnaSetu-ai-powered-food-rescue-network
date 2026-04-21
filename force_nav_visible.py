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
    
    # 1. Update cache buster for ai_assistant.js
    content = re.sub(r'src="ai_assistant\.js(\?v=\d+)?"', 'src="ai_assistant.js?v=4"', content)
    
    # 2. Add inline styles to the mobile nav to force visibility just in case tailwind purged it or z-index conflicted
    # Look for the nav injected earlier
    # We will just replace exactly the class string that was broken or enhance it.
    old_nav_class = 'class="md:hidden fixed bottom-0 left-0 right-0 bg-white/95 dark:bg-[#121629]/95 backdrop-blur-xl border-t border-gray-200 dark:border-white/10 z-[100] flex justify-around items-center h-16 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] pb-[env(safe-area-inset-bottom)]"'
    
    new_nav_class = 'class="md:hidden fixed bottom-0 left-0 right-0 bg-white/95 dark:bg-[#121629]/95 backdrop-blur-xl border-t border-gray-200 dark:border-white/10 flex justify-around items-center h-16 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] pb-[env(safe-area-inset-bottom)]" style="z-index: 9999 !important;"'
    
    content = content.replace(old_nav_class, new_nav_class)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Updated 5 pages with force-visible nav and cache buster.")
