#!/usr/bin/env python3
"""
Reusable category page generator for whichfoodtoavoid.com.
Generates category HTML pages from data/categories.json product data.
Usage: python3 generate_category_page.py [category_slug]
If no slug provided, regenerates all category pages that have products.
"""

import json
import os
import sys
import html as html_lib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'categories.json')
CATEGORIES_DIR = os.path.join(BASE_DIR, 'categories')

SITE_HEAD = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{og_description}">
<meta property="og:image" content="https://whichfoodtoavoid.com/og-image.png">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><rect width='40' height='40' rx='3' fill='%230d1117'/><text x='7' y='28' font-family='sans-serif' font-size='22' fill='%2322d3ee'>W</text></svg>">
<style>
:root{{--bg:#0d1117;--card:#1c2128;--p:#22d3ee;--t:#e6edf3;--t2:#8d96a0;--bd:#30363d;--green:#3fb950;--yellow:#d29922;--red:#f85149}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--t);line-height:1.6}}
.container{{max-width:900px;margin:0 auto;padding:20px}}
header{{text-align:center;padding:40px 20px 20px}}
.logo{{font-size:2rem;font-weight:800;color:var(--p)}}
.logo a{{color:var(--p);text-decoration:none}}
.tagline{{color:var(--t2);font-size:0.9rem;margin-top:4px}}
.section{{margin:30px 0}}
h2{{color:var(--p);font-size:1.2rem;margin-bottom:15px;border-bottom:1px solid var(--bd);padding-bottom:8px}}
h3{{color:var(--t);font-size:1.05rem;margin-bottom:8px}}
.grid{{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(280px,1fr))}}
.card{{background:var(--card);border:1px solid var(--bd);border-radius:8px;padding:18px;transition:border-color 0.2s}}
.card:hover{{border-color:var(--p)}}
.card h3{{font-size:1rem;margin-bottom:6px}}
.card p{{color:var(--t2);font-size:0.85rem;margin-bottom:6px}}
.price{{color:var(--green);font-weight:600;font-size:1.1rem}}
.rating{{color:var(--yellow);font-size:0.9rem}}
.rating-stars{{color:var(--yellow)}}
.btn{{display:inline-block;background:var(--p);color:var(--bg);padding:6px 14px;border-radius:5px;text-decoration:none;font-size:0.85rem;font-weight:600;margin-top:8px}}
.btn:hover{{opacity:0.9}}
.product-meta{{display:flex;gap:15px;flex-wrap:wrap;margin:6px 0}}
.product-meta span{{font-size:0.85rem;color:var(--t2)}}
.comparison-table{{width:100%;border-collapse:collapse;margin:15px 0;font-size:0.9rem}}
.comparison-table th,.comparison-table td{{border:1px solid var(--bd);padding:10px 12px;text-align:left}}
.comparison-table th{{background:var(--card);color:var(--p);font-weight:600}}
.comparison-table tr:nth-child(even){{background:rgba(255,255,255,0.02)}}
.comparison-link{{color:var(--p);text-decoration:none;font-size:0.85rem}}
.comparison-link:hover{{text-decoration:underline}}
.category-icon{{font-size:2rem;display:block;text-align:center;margin-bottom:5px}}
.back-link{{display:inline-block;margin-bottom:20px;color:var(--p);text-decoration:none;font-size:0.9rem}}
.back-link:hover{{text-decoration:underline}}
footer{{text-align:center;padding:30px;color:var(--t2);font-size:0.85rem;border-top:1px solid var(--bd);margin-top:40px}}
</style>
</head>
<body>
<div class="container">
<header><div class="logo"><a href="/">Which Food To Avoid</a></div><p class="tagline">{tagline}</p></header>
<a href="/" class="back-link">&larr; Back to Home</a>
<div class="section">
'''

SITE_FOOT = '''</div>
<footer><p>(c) 2026 WhichFoodToAvoid.com - Evidence-based nutrition information. Not medical advice. As an Amazon Associate we earn from qualifying purchases.</p></footer>
</div>
</body>
</html>'''


def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def rating_stars(rating):
    try:
        r = float(rating)
        full = int(r)
        half = 1 if r - full >= 0.5 else 0
        empty = 5 - full - half
        return '★' * full + ('½' if half else '') + '☆' * empty
    except (ValueError, TypeError):
        return ''


def escape(s):
    return html_lib.escape(str(s))


def generate_category_page(category_slug, data=None):
    if data is None:
        data = load_data()
    
    cat_info = data['categories'].get(category_slug)
    if not cat_info:
        print(f"Category '{category_slug}' not found in data.")
        return False
    
    products = data['products'].get(category_slug, [])
    
    title = f"{cat_info['icon']} Best {cat_info['name']} - Which Food To Avoid"
    description = f"Compare the best {cat_info['name'].lower()}. {cat_info['desc']} - unbiased reviews and comparisons with Amazon UK affiliate links."
    
    html = SITE_HEAD.format(
        title=escape(title),
        description=escape(description),
        og_title=escape(f"Best {cat_info['name']} - Which Food To Avoid"),
        og_description=escape(description),
        tagline=f"{cat_info['icon']} {escape(cat_info['name'])} - {escape(cat_info['desc'])}"
    )
    
    if not products:
        html += f'<p style="color:var(--t2);font-size:0.9rem">No products listed yet. Check back soon for comparisons!</p>\n'
    else:
        html += f'<h2>{cat_info["icon"]} Best {escape(cat_info["name"])}</h2>\n'
        html += f'<p style="color:var(--t2);font-size:0.85rem;margin-bottom:15px">Compare top-rated {escape(cat_info["name"].lower())} from Amazon UK. Prices and availability may change.</p>\n'
        
        # Check for existing comparison files
        comparisons_dir = os.path.join(BASE_DIR, 'comparisons')
        comparison_files = []
        if os.path.isdir(comparisons_dir):
            for f in os.listdir(comparisons_dir):
                if f.startswith(f'comparison-{category_slug}-') and f.endswith('.html'):
                    comparison_files.append(f)
            comparison_files.sort(reverse=True)
        
        if comparison_files:
            html += '<h3>Latest Comparisons</h3>\n'
            for cf in comparison_files[:3]:
                date_part = cf.replace(f'comparison-{category_slug}-', '').replace('.html', '')
                html += f'<p><a href="/comparisons/{escape(cf)}" class="comparison-link">📊 Comparison from {escape(date_part)}</a></p>\n'
        
        # Product cards
        html += '<div class="grid">\n'
        for prod in products:
            name = prod.get('name', 'Unknown Product')
            price = prod.get('price', 'Check Amazon')
            rating = prod.get('rating', '')
            url = prod.get('url', '#')
            asin = prod.get('asin', '')
            date_added = prod.get('date_added', '')
            
            html += '<div class="card">\n'
            html += f'<h3>{escape(name)}</h3>\n'
            html += '<div class="product-meta">\n'
            html += f'<span class="price">{escape(price)}</span>\n'
            if rating:
                stars = rating_stars(rating)
                html += f'<span class="rating">{stars} {escape(str(rating))}</span>\n'
            if asin:
                html += f'<span>ASIN: {escape(asin)}</span>\n'
            if date_added:
                html += f'<span>Added: {escape(date_added)}</span>\n'
            html += '</div>\n'
            html += f'<a href="{escape(url)}" class="btn" target="_blank" rel="nofollow sponsored">Check Price on Amazon →</a>\n'
            html += '</div>\n'
        html += '</div>\n'
    
    html += SITE_FOOT
    
    os.makedirs(CATEGORIES_DIR, exist_ok=True)
    out_path = os.path.join(CATEGORIES_DIR, f'{category_slug}.html')
    with open(out_path, 'w') as f:
        f.write(html)
    
    print(f"✓ Generated category page: {out_path}")
    return True


def main():
    os.makedirs(CATEGORIES_DIR, exist_ok=True)
    data = load_data()
    
    if len(sys.argv) > 1:
        # Generate specific category
        slug = sys.argv[1]
        generate_category_page(slug, data)
    else:
        # Generate all categories that have products
        generated = 0
        for slug in data['products']:
            if data['products'][slug]:
                if generate_category_page(slug, data):
                    generated += 1
        if generated == 0:
            print("No categories with products found. Run the comparison script first or use: python3 generate_category_page.py <slug>")


if __name__ == '__main__':
    main()
