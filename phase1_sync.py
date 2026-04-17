import os
import re

files = [
    'Admin_Dashboard.html',
    'Donation_Interface.html',
    'Volunteer_Logistics.html',
    'Impact_Hub.html'
]

replacements = {
    # 1. Navbar: Make it blend with the page background
    r'bg-\[#faf6f0\]/90 dark:bg-\[#0B0F19\]/90': r'bg-[#faf6f0]/90 dark:bg-[#0B0F19]/90', # Already mostly correct but ensuring transparency
    r'bg-\[#121629\]/95': r'bg-[#faf6f0]/90 dark:bg-[#0B0F19]/90', 
    
    # 2. Main Body Background
    r'<body class=\"bg-background text-on-surface dark:text-slate-200\"': r'<body class=\"bg-[#faf6f0] dark:bg-[#0B0F19] text-on-surface dark:text-slate-200 antialiased\"',
    r'<body class=\"bg-surface text-on-surface dark:text-slate-200\"': r'<body class=\"bg-[#faf6f0] dark:bg-[#0B0F19] text-on-surface dark:text-slate-200 antialiased\"',
    r'bg-surface-container-lowest dark:bg-[#121629]': r'bg-surface-container-lowest dark:bg-[#121629] dark:border-white/5',
}

for filename in files:
    if not os.path.exists(filename): continue
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = re.sub(old, new, content)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("Phase 1: Global Theme Sync Complete.")
