#!/usr/bin/env python3
"""
Text Sitemap Generator for OmniTrends

Creates a simple text-based sitemap that Google Search Console can easily fetch.
Text sitemaps are often more reliable than XML on GitHub Pages.
"""

import json
import os
from datetime import datetime

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

def generate_text_sitemap():
    """Generate a simple text-based sitemap."""
    print("📝 Generating text-based sitemap...")
    
    # Load data
    articles = load_json_data('articles.json')
    categories_data = load_json_data('categories.json')
    categories = categories_data.get('categories', []) if isinstance(categories_data, dict) else []
    
    print(f"📄 Found {len(articles)} articles and {len(categories)} categories")
    
    # Collect all URLs
    urls = []
    
    # 1. Homepage
    urls.append(f"{BASE_URL}/")
    
    # 2. Main pages
    main_pages = [
        'pages/about.html',
        'pages/contact.html',
        'pages/privacy.html',
        'pages/terms.html',
        'pages/disclaimer.html'
    ]
    
    for page_path in main_pages:
        full_path = os.path.join(PROJECT_ROOT, page_path)
        if os.path.exists(full_path):
            urls.append(f"{BASE_URL}/{page_path}")
    
    # 3. Category pages
    for category in categories:
        category_slug = category.get('slug', '').lower()
        if category_slug:
            category_path = f"category/{category_slug}.html"
            full_path = os.path.join(PROJECT_ROOT, category_path)
            
            if os.path.exists(full_path):
                urls.append(f"{BASE_URL}/{category_path}")
    
    # 4. Article pages
    for article in articles:
        article_id = article.get('id')
        if article_id:
            article_path = f"articles/{article_id}.html"
            full_path = os.path.join(PROJECT_ROOT, article_path)
            
            if os.path.exists(full_path):
                urls.append(f"{BASE_URL}/{article_path}")
    
    # Write text sitemap
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.txt')
    
    try:
        with open(sitemap_path, 'w', encoding='utf-8', newline='\n') as f:
            for url in urls:
                f.write(url + '\n')
        
        print(f"✅ Text sitemap generated successfully!")
        print(f"📍 Location: {sitemap_path}")
        print(f"📊 Total URLs: {len(urls)}")
        
        # Show file size
        file_size = os.path.getsize(sitemap_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing sitemap: {e}")
        return False

def main():
    """Main function."""
    print("🚀 OmniTrends Text Sitemap Generator")
    print("=" * 40)
    
    success = generate_text_sitemap()
    
    if success:
        print("\n" + "=" * 40)
        print("📋 Next Steps:")
        print("1. Commit and push sitemap.txt to GitHub")
        print("2. Update robots.txt to reference sitemap.txt")
        print("3. Submit sitemap.txt to Google Search Console")
        print("4. URL: https://omnitrends.github.io/sitemap.txt")
    else:
        print("❌ Text sitemap generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())