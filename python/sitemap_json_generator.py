#!/usr/bin/env python3
"""
JSON Sitemap Generator for OmniTrends

Creates a JSON-based sitemap that can be easily served and consumed.
"""

import json
import os
from datetime import datetime, timezone

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
    """Format date for sitemap."""
    if date_string:
        try:
            # Parse "31 July 2025" format
            parsed_date = datetime.strptime(date_string.strip(), '%d %B %Y')
            return parsed_date.strftime('%Y-%m-%d')
        except:
            pass
    
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

def generate_json_sitemap():
    """Generate JSON-based sitemap."""
    print("📝 Generating JSON-based sitemap...")
    
    # Load data
    articles = load_json_data('articles.json')
    categories_data = load_json_data('categories.json')
    categories = categories_data.get('categories', []) if isinstance(categories_data, dict) else []
    
    print(f"📄 Found {len(articles)} articles and {len(categories)} categories")
    
    # Build sitemap structure
    sitemap = {
        "sitemap": {
            "generated": datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00'),
            "base_url": BASE_URL,
            "total_urls": 0,
            "urls": []
        }
    }
    
    # 1. Homepage
    index_date = get_file_date(os.path.join(PROJECT_ROOT, 'index.html'))
    sitemap["sitemap"]["urls"].append({
        "loc": f"{BASE_URL}/",
        "lastmod": index_date,
        "changefreq": "daily",
        "priority": 1.0,
        "type": "homepage"
    })
    
    # 2. Main pages
    main_pages = [
        ('pages/about.html', 'monthly', 0.8, 'page'),
        ('pages/contact.html', 'monthly', 0.7, 'page'),
        ('pages/privacy.html', 'yearly', 0.5, 'page'),
        ('pages/terms.html', 'yearly', 0.5, 'page'),
        ('pages/disclaimer.html', 'yearly', 0.5, 'page')
    ]
    
    for page_path, changefreq, priority, page_type in main_pages:
        full_path = os.path.join(PROJECT_ROOT, page_path)
        if os.path.exists(full_path):
            page_date = get_file_date(full_path)
            sitemap["sitemap"]["urls"].append({
                "loc": f"{BASE_URL}/{page_path}",
                "lastmod": page_date,
                "changefreq": changefreq,
                "priority": priority,
                "type": page_type
            })
    
    # 3. Category pages
    for category in categories:
        category_slug = category.get('slug', '').lower()
        if category_slug:
            category_path = f"category/{category_slug}.html"
            full_path = os.path.join(PROJECT_ROOT, category_path)
            
            if os.path.exists(full_path):
                cat_date = get_file_date(full_path)
                sitemap["sitemap"]["urls"].append({
                    "loc": f"{BASE_URL}/{category_path}",
                    "lastmod": cat_date,
                    "changefreq": "weekly",
                    "priority": 0.8,
                    "type": "category",
                    "category_name": category.get('name', '')
                })
    
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
                priority = 0.9 if is_featured else 0.7
                
                sitemap["sitemap"]["urls"].append({
                    "loc": f"{BASE_URL}/{article_path}",
                    "lastmod": article_date,
                    "changefreq": "monthly",
                    "priority": priority,
                    "type": "article",
                    "title": article.get('title', ''),
                    "category": article.get('category', ''),
                    "featured": is_featured
                })
    
    # Update total count
    sitemap["sitemap"]["total_urls"] = len(sitemap["sitemap"]["urls"])
    
    # Write JSON sitemap
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.json')
    
    try:
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            json.dump(sitemap, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON sitemap generated successfully!")
        print(f"📍 Location: {sitemap_path}")
        print(f"📊 Total URLs: {sitemap['sitemap']['total_urls']}")
        
        # Show file size
        file_size = os.path.getsize(sitemap_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing sitemap: {e}")
        return False

def main():
    """Main function."""
    print("🚀 OmniTrends JSON Sitemap Generator")
    print("=" * 40)
    
    success = generate_json_sitemap()
    
    if success:
        print("\n" + "=" * 40)
        print("📋 Usage:")
        print("1. This creates a machine-readable sitemap")
        print("2. Can be used by custom crawlers or tools")
        print("3. URL: https://omnitrends.github.io/sitemap.json")
    else:
        print("❌ JSON sitemap generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())