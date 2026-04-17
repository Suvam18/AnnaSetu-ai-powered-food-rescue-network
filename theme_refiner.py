import os
import re

files = [
    'Admin_Dashboard.html',
    'Donation_Interface.html',
    'Volunteer_Logistics.html',
    'Impact_Hub.html'
]

replacements = {
    # 1. Fix the Navbar Background to be an extension of the page
    r'bg-white/90 dark:bg-\[\#121629\]/95': 
        r'bg-[#faf6f0]/90 dark:bg-[#0B0F19]/90',
        
    # 2. Upgrade the boring "stone" dark mode to Cinematic Dark Blue
    r'dark:bg-stone-950': r'dark:bg-[#0B0F19]',
    r'dark:bg-stone-900': r'dark:bg-[#121629]',
    r'dark:bg-stone-800': r'dark:bg-[#1A1F35]',
    r'dark:bg-stone-700': r'dark:bg-[#242A45]',
    
    r'dark:border-stone-800': r'dark:border-white/10',
    r'dark:border-stone-700': r'dark:border-white/20',
    
    # 3. Increase text coolness in dark mode (slightly blueish white)
    r'dark:text-stone-100': r'dark:text-slate-100',
    r'dark:text-stone-200': r'dark:text-slate-200',
    r'dark:text-stone-300': r'dark:text-slate-300',
    r'dark:text-stone-400': r'dark:text-slate-400',
}

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = re.sub(old, new, content)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print(f'Updated {len(files)} files to cinematic dark mode and extended navbar!')
