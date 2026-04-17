import os
import re

files = [
    'Admin_Dashboard.html',
    'Donation_Interface.html',
    'Volunteer_Logistics.html',
    'Impact_Hub.html'
]

replacements = {
    # 1. Navbar Container
    r'bg-\[\#121629\]/95 backdrop-blur-xl border border-white/10 rounded-full shadow-\[0_8px_32px_rgba\(0,0,0,0\.3\)\]': 
        r'bg-white/90 dark:bg-[#121629]/95 backdrop-blur-xl border border-stone-200/50 dark:border-white/10 rounded-full shadow-lg dark:shadow-[0_8px_32px_rgba(0,0,0,0.3)]',
    
    # 2. Navbar Logo Text
    r'text-white\s*\">AnnaSetu': 
        r'text-emerald-900 dark:text-white\">AnnaSetu',
    
    # 3. Navbar Links
    r'text-gray-300 font-semibold hover:text-\[\#facc15\]': 
        r'text-stone-600 dark:text-gray-300 font-semibold hover:text-emerald-700 dark:hover:text-[#facc15]',
    
    # 4. Navbar Theme Button
    r'bg-\[\#1e243b\] hover:bg-\[\#2a304a\]': 
        r'bg-stone-100 dark:bg-[#1e243b] hover:bg-stone-200 dark:hover:bg-[#2a304a]',
    r'text-gray-300 hover:text-white transition-colors border border-white/5': 
        r'text-stone-600 hover:text-stone-900 dark:text-gray-300 dark:hover:text-white transition-colors border border-stone-200 dark:border-white/5',
        
    # 5. Full Page Dark Mode Body
    r'<body class=\"bg-background text-on-surface': 
        r'<body class=\"bg-background dark:bg-stone-950 text-on-surface dark:text-stone-200',
    r'<body class=\"bg-surface text-on-surface': 
        r'<body class=\"bg-surface dark:bg-stone-950 text-on-surface dark:text-stone-200',
        
    # 6. Global Background Colors
    r'bg-surface\b(?!-container)(?! dark:)': r'bg-surface dark:bg-stone-900',
    r'bg-surface-container-lowest\b(?! dark:)': r'bg-surface-container-lowest dark:bg-stone-900',
    r'bg-surface-container-low\b(?! dark:)': r'bg-surface-container-low dark:bg-stone-800',
    r'bg-surface-container\b(?!-low)(?!-high)(?! dark:)': r'bg-surface-container dark:bg-stone-800',
    r'bg-surface-container-highest\b(?! dark:)': r'bg-surface-container-highest dark:bg-stone-700',
    
    # 7. Global Text Colors
    r'text-on-surface\b(?!-)(?! dark:)': r'text-on-surface dark:text-stone-100',
    r'text-on-surface-variant\b(?! dark:)': r'text-on-surface-variant dark:text-stone-300',
    r'text-secondary\b(?!-)(?! dark:)': r'text-secondary dark:text-stone-400',
    
    # 8. Border classes missing dark fallback
    r'border-outline-variant/10\b(?! dark:)': r'border-outline-variant/10 dark:border-stone-800',
    r'border-outline-variant/30\b(?! dark:)': r'border-outline-variant/30 dark:border-stone-700',
}

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = re.sub(old, new, content)
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print(f'Updated {len(files)} files with full page dark mode logic!')
