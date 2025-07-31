#!/usr/bin/env python3
"""
Simple and Robust Sitemap Generator for OmniTrends GitHub Pages

This generator creates a clean, Google Search Console compatible sitemap.xml
that addresses common fetching issues.
"""

import json
import os
from datetime import datetime, timezone
from urllib.parse import quote

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Website base URL for GitHub Pages
BASE_URL = "https://omnitrends.github.io"

def load_json_data(filename):
    """Load JSON data from file."""
    file_path = os.path.join(PROJECT_ROOT, 'json', filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load {filename}: {e}")
        return [] if filename == 'articles.json' else {'categories': []}

def format_date(date_string=None):
    """Format date for sitemap (YYYY-MM-DD format is preferred by Google)."""
    if date_string:
        try:
            # Parse "31 July 2025" format
            parsed_date = datetime.strptime(date_string.strip(), '%d %B %Y')
            return parsed_date.strftime('%Y-%m-%d')
        except:
            pass
    
    # Return current date
    return datetime.now().strftime('%Y-%m-%d')

def get_file_date(file_path):
    """Get file modification date."""
    try:
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except:
        pass
    return datetime.now().strftime('%Y-%m-%d')

def generate_sitemap():
    """Generate XML sitemap."""
    print("🗺️  Generating sitemap for OmniTrends...")
    
    # Load data
    articles = load_json_data('articles.json')
    categories_data = load_json_data('categories.json')
    categories = categories_data.get('categories', []) if isinstance(categories_data, dict) else []
    
    print(f"📄 Found {len(articles)} articles and {len(categories)} categories")
    
    # Start building sitemap XML
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    # 1. Homepage
    index_date = get_file_date(os.path.join(PROJECT_ROOT, 'index.html'))
    sitemap_lines.extend([
        '  <url>',
        f'    <loc>{BASE_URL}/</loc>',
        f'    <lastmod>{index_date}</lastmod>',
        '    <changefreq>daily</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>'
    ])
    
    # 2. Main pages
    main_pages = [
        ('pages/about.html', 'monthly', '0.8'),
        ('pages/contact.html', 'monthly', '0.7'),
        ('pages/privacy.html', 'yearly', '0.5'),
        ('pages/terms.html', 'yearly', '0.5'),
        ('pages/disclaimer.html', 'yearly', '0.5')
    ]
    
    for page_path, changefreq, priority in main_pages:
        full_path = os.path.join(PROJECT_ROOT, page_path)
        if os.path.exists(full_path):
            page_date = get_file_date(full_path)
            sitemap_lines.extend([
                '  <url>',
                f'    <loc>{BASE_URL}/{page_path}</loc>',
                f'    <lastmod>{page_date}</lastmod>',
                f'    <changefreq>{changefreq}</changefreq>',
                f'    <priority>{priority}</priority>',
                '  </url>'
            ])
    
    # 3. Category pages
    for category in categories:
        category_slug = category.get('slug', '').lower()
        if category_slug:
            category_path = f"category/{category_slug}.html"
            full_path = os.path.join(PROJECT_ROOT, category_path)
            
            if os.path.exists(full_path):
                cat_date = get_file_date(full_path)
                sitemap_lines.extend([
                    '  <url>',
                    f'    <loc>{BASE_URL}/{category_path}</loc>',
                    f'    <lastmod>{cat_date}</lastmod>',
                    '    <changefreq>weekly</changefreq>',
                    '    <priority>0.8</priority>',
                    '  </url>'
                ])
    
    # 4. Article pages
    for article in articles:
        article_id = article.get('id')
        if article_id:
            article_path = f"articles/{article_id}.html"
            full_path = os.path.join(PROJECT_ROOT, article_path)
            
            if os.path.exists(full_path):
                # Use article date if available, otherwise file date
                article_date = format_date(article.get('date'))
                
                # Featured articles get higher priority
                is_featured = article.get('featured', False)
                priority = '0.9' if is_featured else '0.7'
                
                sitemap_lines.extend([
                    '  <url>',
                    f'    <loc>{BASE_URL}/{article_path}</loc>',
                    f'    <lastmod>{article_date}</lastmod>',
                    '    <changefreq>monthly</changefreq>',
                    f'    <priority>{priority}</priority>',
                    '  </url>'
                ])
    
    # Close sitemap
    sitemap_lines.append('</urlset>')
    
    # Write sitemap
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    try:
        with open(sitemap_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sitemap_lines))
        
        print(f"✅ Sitemap generated successfully!")
        print(f"📍 Location: {sitemap_path}")
        print(f"📊 Total URLs: {len([line for line in sitemap_lines if '<loc>' in line])}")
        
        # Show file size
        file_size = os.path.getsize(sitemap_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing sitemap: {e}")
        return False

def validate_sitemap():
    """Basic sitemap validation."""
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    if not os.path.exists(sitemap_path):
        print("❌ Sitemap file not found")
        return False
    
    try:
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic checks
        if not content.startswith('<?xml'):
            print("⚠️  Warning: Missing XML declaration")
        
        if 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' not in content:
            print("⚠️  Warning: Missing or incorrect namespace")
        
        url_count = content.count('<loc>')
        print(f"✅ Sitemap validation passed")
        print(f"📊 Found {url_count} URLs")
        
        return True
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 OmniTrends Sitemap Generator v2")
    print("=" * 40)
    
    success = generate_sitemap()
    
    if success:
        print("\n" + "=" * 40)
        print("🔍 Validating sitemap...")
        validate_sitemap()
        
        print("\n" + "=" * 40)
        print("📋 Next Steps:")
        print("1. Commit and push sitemap.xml to GitHub")
        print("2. Wait for GitHub Pages to deploy")
        print("3. Test sitemap URL: https://omnitrends.github.io/sitemap.xml")
        print("4. Resubmit to Google Search Console")
        print("5. Check robots.txt includes sitemap reference")
    else:
        print("❌ Sitemap generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())