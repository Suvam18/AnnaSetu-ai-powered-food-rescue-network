import os

files = ['Admin_Dashboard.html', 'Donation_Interface.html', 'Volunteer_Logistics.html', 'Impact_Hub.html']

for fn in files:
    with open(fn, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Fix the typo "\"AnnaSetu" -> ""AnnaSetu"
    c = c.replace(r'\">AnnaSetu', '">AnnaSetu')
    
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(c)
