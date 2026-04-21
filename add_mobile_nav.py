import os
import re

files = [
    ("Restaurant_Portal_Dashboard.html", "dashboard", "Dashboard"),
    ("Excess_Notification_Center.html", "inventory_2", "Surplus log"),
    ("Restaurant_Locations_Management.html", "pin_drop", "Locations"),
    ("Restaurant_Analytics_and_Impact.html", "insert_chart", "Analytics"),
    ("Restaurant_Team_Management.html", "groups", "Team")
]

dir_path = r"c:\Users\User\OneDrive\Desktop\AnnaSetu\AnnaSetu-ai-powered-food-rescue-network"

# CSS addition for body padding on mobile
css_addition = """
  @media (max-width: 768px) {
    body { padding-bottom: 6rem; }
  }
"""

def generate_nav(current_file):
    nav_html = '\n<!-- Mobile Bottom Navigation -->\n<nav class="md:hidden fixed bottom-0 left-0 right-0 bg-white/95 dark:bg-[#121629]/95 backdrop-blur-xl border-t border-gray-200 dark:border-white/10 z-[100] flex justify-around items-center h-16 shadow-[0_-4px_20px_rgba(0,0,0,0.05)] pb-[env(safe-area-inset-bottom)]">\n'
    
    for filename, icon, label in files:
        is_active = (filename == current_file)
        
        # Color classes
        if is_active:
            text_color = "text-[#4a7c59] dark:text-[#facc15]"
            fill_style = "style=\"font-variation-settings:'FILL' 1\""
        else:
            text_color = "text-stone-500 hover:text-[#4a7c59] dark:text-stone-400 dark:hover:text-[#facc15]"
            fill_style = ""

        badge_html = ""
        if filename == "Restaurant_Locations_Management.html":
            badge_html = '\n        <span id="mobile-nav-loc-badge" class="hidden absolute top-1 right-3 min-w-[14px] h-3.5 px-0.5 bg-red-500 text-white text-[8px] font-black rounded-full flex items-center justify-center shadow-sm animate-pulse">0</span>'

        nav_html += f"""    <a href="{filename}" class="flex flex-col items-center justify-center w-full h-full {text_color} transition-colors relative group">
        <span class="material-symbols-outlined text-2xl group-hover:scale-110 transition-transform" {fill_style}>{icon}</span>
        <span class="text-[9px] font-bold mt-0.5 tracking-wide">{label}</span>{badge_html}
    </a>
"""
    nav_html += "</nav>\n"
    return nav_html

for filename, _, _ in files:
    filepath = os.path.join(dir_path, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Remove old mobile nav if exists
    content = re.sub(r'<!-- Mobile Bottom Navigation -->.*?<\/nav>', '', content, flags=re.DOTALL)
    
    # Add new nav right before </body>
    if '</body>' in content:
        content = content.replace('</body>', generate_nav(filename) + '</body>')
        
    # Ensure body has mobile padding by adding to style tag if not present
    if '@media (max-width: 768px) { body' not in content and 'body { padding-bottom: 6rem; }' not in content:
        if '</style>' in content:
            content = content.replace('</style>', css_addition + '</style>')
            
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename} with mobile nav.")
