#!/usr/bin/env python3
"""
Sitemap Generator for OmniTrends GitHub Pages Website

This script generates a comprehensive XML sitemap for the OmniTrends website
hosted on GitHub Pages. It includes all pages, articles, and categories with
proper SEO attributes like priority, changefreq, and lastmod dates.

The sitemap follows the XML Sitemap Protocol 0.9 specification:
https://www.sitemaps.org/protocol.html
"""

import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import quote

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Website base URL for GitHub Pages
BASE_URL = "https://omnitrends.github.io"

def get_file_modification_date(file_path):
    """
    Get the last modification date of a file.
    Returns ISO format date string or current date if file doesn't exist.
    """
    try:
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        else:
            return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    except Exception:
        return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')

def load_articles_data():
    """Load articles data from JSON file."""
    articles_path = os.path.join(PROJECT_ROOT, 'json', 'articles.json')
    try:
        with open(articles_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load articles.json: {e}")
        return []

def load_categories_data():
    """Load categories data from JSON file."""
    categories_path = os.path.join(PROJECT_ROOT, 'json', 'categories.json')
    try:
        with open(categories_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('categories', [])
    except Exception as e:
        print(f"Warning: Could not load categories.json: {e}")
        return []

def parse_article_date(date_string):
    """
    Parse article date string and convert to ISO format.
    Handles various date formats from the articles.json.
    """
    try:
        # Try to parse "31 July 2025" format
        if date_string:
            # Remove any extra whitespace
            date_string = date_string.strip()
            
            # Parse the date
            parsed_date = datetime.strptime(date_string, '%d %B %Y')
            
            # Convert to UTC timezone and set to noon to avoid timezone issues
            parsed_date = parsed_date.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
            
            return parsed_date.strftime('%Y-%m-%dT%H:%M:%S+00:00')
    except Exception:
        pass
    
    # Fallback to current date at noon
    current = datetime.now(timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
    return current.strftime('%Y-%m-%dT%H:%M:%S+00:00')

def create_url_element(parent, loc, lastmod=None, changefreq=None, priority=None):
    """
    Create a URL element for the sitemap with all sub-elements.
    
    Args:
        parent: Parent XML element
        loc: URL location (required)
        lastmod: Last modification date (optional)
        changefreq: Change frequency (optional)
        priority: Priority (optional)
    """
    url_elem = ET.SubElement(parent, 'url')
    
    # Location (required)
    loc_elem = ET.SubElement(url_elem, 'loc')
    loc_elem.text = loc
    
    # Last modification date (optional)
    if lastmod:
        lastmod_elem = ET.SubElement(url_elem, 'lastmod')
        lastmod_elem.text = lastmod
    
    # Change frequency (optional)
    if changefreq:
        changefreq_elem = ET.SubElement(url_elem, 'changefreq')
        changefreq_elem.text = changefreq
    
    # Priority (optional)
    if priority:
        priority_elem = ET.SubElement(url_elem, 'priority')
        priority_elem.text = str(priority)

def generate_sitemap():
    """Generate the complete XML sitemap."""
    print("Starting sitemap generation...")
    
    # Create root element with namespace
    urlset = ET.Element('urlset')
    urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Load data
    articles = load_articles_data()
    categories = load_categories_data()
    
    print(f"Loaded {len(articles)} articles and {len(categories)} categories")
    
    # 1. Add homepage (highest priority)
    index_path = os.path.join(PROJECT_ROOT, 'index.html')
    if os.path.exists(index_path):
        index_lastmod = get_file_modification_date(index_path)
        create_url_element(
            urlset,
            f"{BASE_URL}/",
            lastmod=index_lastmod,
            changefreq="daily",
            priority=1.0
        )
        print("Added homepage to sitemap")
    else:
        # Add homepage even if file doesn't exist (for GitHub Pages)
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
        create_url_element(
            urlset,
            f"{BASE_URL}/",
            lastmod=current_time,
            changefreq="daily",
            priority=1.0
        )
        print("Added homepage to sitemap (file not found, using current time)")
    
    # 2. Add main pages
    main_pages = [
        ('pages/about.html', 'about', 'monthly', 0.8),
        ('pages/contact.html', 'contact', 'monthly', 0.7),
        ('pages/privacy.html', 'privacy', 'yearly', 0.5),
        ('pages/terms.html', 'terms', 'yearly', 0.5),
        ('pages/disclaimer.html', 'disclaimer', 'yearly', 0.5),
    ]
    
    for page_path, page_name, changefreq, priority in main_pages:
        full_path = os.path.join(PROJECT_ROOT, page_path)
        if os.path.exists(full_path):
            lastmod = get_file_modification_date(full_path)
            create_url_element(
                urlset,
                f"{BASE_URL}/{page_path}",
                lastmod=lastmod,
                changefreq=changefreq,
                priority=priority
            )
            print(f"Added {page_name} page to sitemap")
    
    # 3. Add category pages
    for category in categories:
        category_slug = category.get('slug', '').lower()
        if category_slug:
            category_path = f"category/{category_slug}.html"
            full_path = os.path.join(PROJECT_ROOT, category_path)
            
            if os.path.exists(full_path):
                lastmod = get_file_modification_date(full_path)
                create_url_element(
                    urlset,
                    f"{BASE_URL}/{category_path}",
                    lastmod=lastmod,
                    changefreq="weekly",
                    priority=0.8
                )
                print(f"Added category '{category.get('name')}' to sitemap")
    
    # 4. Add article pages
    for article in articles:
        article_id = article.get('id')
        article_date = article.get('date')
        
        if article_id:
            article_path = f"articles/{article_id}.html"
            full_path = os.path.join(PROJECT_ROOT, article_path)
            
            if os.path.exists(full_path):
                # Use article date if available, otherwise file modification date
                if article_date:
                    lastmod = parse_article_date(article_date)
                else:
                    lastmod = get_file_modification_date(full_path)
                
                # Featured articles get higher priority
                is_featured = article.get('featured', False)
                priority = 0.9 if is_featured else 0.7
                
                create_url_element(
                    urlset,
                    f"{BASE_URL}/{article_path}",
                    lastmod=lastmod,
                    changefreq="monthly",
                    priority=priority
                )
                print(f"Added article '{article.get('title', article_id)}' to sitemap")
    
    # 5. Add robots.txt if it exists
    robots_path = os.path.join(PROJECT_ROOT, 'robots.txt')
    if os.path.exists(robots_path):
        lastmod = get_file_modification_date(robots_path)
        create_url_element(
            urlset,
            f"{BASE_URL}/robots.txt",
            lastmod=lastmod,
            changefreq="yearly",
            priority=0.1
        )
        print("Added robots.txt to sitemap")
    
    # Create the XML tree
    tree = ET.ElementTree(urlset)
    
    # Format the XML with proper indentation
    ET.indent(tree, space="  ", level=0)
    
    # Write to sitemap.xml in the root directory
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    try:
        # Write with XML declaration and UTF-8 encoding
        with open(sitemap_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
            tree.write(f, encoding='utf-8', xml_declaration=False)
        
        print(f"\n✅ Sitemap successfully generated: {sitemap_path}")
        print(f"📊 Total URLs in sitemap: {len(urlset)}")
        
        # Display file size
        file_size = os.path.getsize(sitemap_path)
        print(f"📁 Sitemap file size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing sitemap: {e}")
        return False

def validate_sitemap():
    """Validate the generated sitemap."""
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    if not os.path.exists(sitemap_path):
        print("❌ Sitemap file not found for validation")
        return False
    
    try:
        # Parse the XML to check if it's valid
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        # Check namespace
        expected_namespace = 'http://www.sitemaps.org/schemas/sitemap/0.9'
        if root.tag != f'{{{expected_namespace}}}urlset':
            print("⚠️  Warning: Sitemap namespace might be incorrect")
        
        # Count URLs
        urls = root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url')
        url_count = len(urls)
        
        print(f"✅ Sitemap validation passed")
        print(f"📊 Validated {url_count} URLs")
        
        # Check for required elements
        missing_loc = 0
        for url in urls:
            loc = url.find('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc is None or not loc.text:
                missing_loc += 1
        
        if missing_loc > 0:
            print(f"⚠️  Warning: {missing_loc} URLs missing location element")
        else:
            print("✅ All URLs have valid location elements")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ Sitemap XML validation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Sitemap validation error: {e}")
        return False

def main():
    """Main function to generate and validate sitemap."""
    print("🗺️  OmniTrends Sitemap Generator")
    print("=" * 50)
    
    # Generate sitemap
    success = generate_sitemap()
    
    if success:
        print("\n" + "=" * 50)
        print("🔍 Validating sitemap...")
        validate_sitemap()
        
        print("\n" + "=" * 50)
        print("📋 Next Steps:")
        print("1. Submit sitemap.xml to Google Search Console")
        print("2. Add sitemap URL to robots.txt if not already present")
        print("3. Monitor sitemap status in search console")
        print(f"4. Sitemap URL: {BASE_URL}/sitemap.xml")
        
    else:
        print("\n❌ Sitemap generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())