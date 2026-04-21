import re

files = [
    ("Restaurant_Portal_Dashboard.html", "dashboard"),
    ("Excess_Notification_Center.html", "surplus"),
    ("Restaurant_Locations_Management.html", "locations"),
    ("Restaurant_Analytics_and_Impact.html", "analytics"),
    ("Restaurant_Team_Management.html", "team"),
]

# Pure CSS nav that does NOT use any Tailwind class for visibility
NAV_CSS = """
<style id="mobile-nav-css">
  #annasetu-mobile-nav {
    display: none;
  }
  @media (max-width: 1024px) {
    #annasetu-mobile-nav {
      display: flex !important;
      position: fixed !important;
      bottom: 0 !important;
      left: 0 !important;
      right: 0 !important;
      width: 100% !important;
      height: 64px !important;
      z-index: 2147483647 !important;
      background-color: rgba(255, 255, 255, 0.98) !important;
      backdrop-filter: blur(20px) !important;
      -webkit-backdrop-filter: blur(20px) !important;
      border-top: 1px solid #e5e7eb !important;
      justify-content: space-around !important;
      align-items: center !important;
      padding-bottom: env(safe-area-inset-bottom) !important;
    }
    #annasetu-mobile-nav a {
      display: flex !important;
      flex-direction: column !important;
      align-items: center !important;
      justify-content: center !important;
      flex: 1 !important;
      height: 100% !important;
      color: #78716c !important;
      text-decoration: none !important;
      font-size: 9px !important;
      font-weight: 700 !important;
      letter-spacing: 0.05em !important;
      transition: color 0.2s !important;
      position: relative !important;
    }
    #annasetu-mobile-nav a:hover {
      color: #4a7c59 !important;
    }
    #annasetu-mobile-nav a.active {
      color: #4a7c59 !important;
    }
    body { padding-bottom: 6rem !important; }
  }
</style>
"""

def make_nav(active_page):
    pages = [
        ("Restaurant_Portal_Dashboard.html", "dashboard", "Dashboard", "dashboard"),
        ("Excess_Notification_Center.html", "surplus", "Surplus log", "inventory_2"),
        ("Restaurant_Locations_Management.html", "locations", "Locations", "pin_drop"),
        ("Restaurant_Analytics_and_Impact.html", "analytics", "Analytics", "insert_chart"),
        ("Restaurant_Team_Management.html", "team", "Team", "groups"),
    ]
    links = ""
    for href, key, label, icon in pages:
        active_class = ' class="active"' if key == active_page else ''
        icon_style = "font-size:24px; font-variation-settings:'FILL' 1" if key == active_page else "font-size:24px;"
        badge = ""
        if key == "locations":
            badge = '<span id="mobile-nav-loc-badge" style="display:none;position:absolute;top:4px;right:12px;min-width:14px;height:14px;padding:0 2px;background:#ef4444;color:#fff;font-size:8px;font-weight:900;border-radius:9999px;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.3);">0</span>'
        links += f"""
    <a href="{href}"{active_class}>
        <span class="material-symbols-outlined" style="{icon_style}">{icon}</span>
        <span>{label}</span>
        {badge}
    </a>"""
    return f'<nav id="annasetu-mobile-nav">{links}\n</nav>'

for filename, active in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any old mobile nav (Tailwind-based or older ones)
    # Pattern: everything from <!-- Mobile Bottom Navigation --> to </nav> (the last one before </body>)
    content = re.sub(
        r'<!-- Mobile Bottom Navigation -->.*?</nav>',
        '',
        content,
        flags=re.DOTALL
    )

    # Also remove old mobile-nav-css if present
    content = re.sub(r'<style id="mobile-nav-css">.*?</style>', '', content, flags=re.DOTALL)

    # Remove old @media padding-bottom rules that were added inline in <style> blocks at bottom
    # (they'll be included in the new CSS)
    content = re.sub(r'\s*@media \(max-width: 768px\) \{\s*body \{ padding-bottom: 6rem; \}\s*\}', '', content)

    # Inject CSS just before </head>
    content = content.replace('</head>', NAV_CSS + '</head>')

    # Inject nav just before </body>
    new_nav = make_nav(active)
    content = content.replace('</body>', f'\n<!-- Mobile Bottom Navigation -->\n{new_nav}\n</body>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"OK: {filename}")

print("\nAll 5 pages fixed with pure-CSS mobile navigation!")
