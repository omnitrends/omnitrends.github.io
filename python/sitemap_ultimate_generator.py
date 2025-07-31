#!/usr/bin/env python3
"""
Ultimate Sitemap Generator for GitHub Pages

This creates multiple sitemap formats and ensures they work with Google Search Console.
It addresses common GitHub Pages XML serving issues.
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

def format_date_iso(date_string=None):
    """Format date in ISO format (YYYY-MM-DD) - most compatible."""
    if date_string:
        try:
            # Parse "31 July 2025" format
            parsed_date = datetime.strptime(date_string.strip(), '%d %B %Y')
            return parsed_date.strftime('%Y-%m-%d')
        except:
            pass
    
    return datetime.now().strftime('%Y-%m-%d')

def get_file_date_iso(file_path):
    """Get file modification date in ISO format."""
    try:
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
    except:
        pass
    return datetime.now().strftime('%Y-%m-%d')

def collect_all_urls():
    """Collect all URLs from the website."""
    print("🔍 Collecting all URLs...")
    
    # Load data
    articles = load_json_data('articles.json')
    categories_data = load_json_data('categories.json')
    categories = categories_data.get('categories', []) if isinstance(categories_data, dict) else []
    
    urls = []
    
    # 1. Homepage
    index_date = get_file_date_iso(os.path.join(PROJECT_ROOT, 'index.html'))
    urls.append({
        'loc': f"{BASE_URL}/",
        'lastmod': index_date,
        'changefreq': 'daily',
        'priority': '1.0',
        'type': 'homepage'
    })
    
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
            page_date = get_file_date_iso(full_path)
            urls.append({
                'loc': f"{BASE_URL}/{page_path}",
                'lastmod': page_date,
                'changefreq': changefreq,
                'priority': priority,
                'type': 'page'
            })
    
    # 3. Category pages
    for category in categories:
        category_slug = category.get('slug', '').lower()
        if category_slug:
            category_path = f"category/{category_slug}.html"
            full_path = os.path.join(PROJECT_ROOT, category_path)
            
            if os.path.exists(full_path):
                cat_date = get_file_date_iso(full_path)
                urls.append({
                    'loc': f"{BASE_URL}/{category_path}",
                    'lastmod': cat_date,
                    'changefreq': 'weekly',
                    'priority': '0.8',
                    'type': 'category'
                })
    
    # 4. Article pages
    for article in articles:
        article_id = article.get('id')
        if article_id:
            article_path = f"articles/{article_id}.html"
            full_path = os.path.join(PROJECT_ROOT, article_path)
            
            if os.path.exists(full_path):
                article_date = format_date_iso(article.get('date'))
                is_featured = article.get('featured', False)
                priority = '0.9' if is_featured else '0.7'
                
                urls.append({
                    'loc': f"{BASE_URL}/{article_path}",
                    'lastmod': article_date,
                    'changefreq': 'monthly',
                    'priority': priority,
                    'type': 'article'
                })
    
    print(f"📊 Collected {len(urls)} URLs")
    return urls

def generate_xml_sitemap(urls):
    """Generate XML sitemap with minimal, clean format."""
    print("📄 Generating XML sitemap...")
    
    # Use the most basic XML format possible
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]
    
    for url in urls:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{url["loc"]}</loc>')
        xml_lines.append(f'    <lastmod>{url["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{url["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{url["priority"]}</priority>')
        xml_lines.append('  </url>')
    
    xml_lines.append('</urlset>')
    
    # Write XML sitemap
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    try:
        # Write with explicit UTF-8 encoding and Unix line endings
        with open(sitemap_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(xml_lines))
        
        print(f"✅ XML sitemap created: {sitemap_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating XML sitemap: {e}")
        return False

def generate_txt_sitemap(urls):
    """Generate simple text sitemap."""
    print("📝 Generating text sitemap...")
    
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.txt')
    
    try:
        with open(sitemap_path, 'w', encoding='utf-8', newline='\n') as f:
            for url in urls:
                f.write(url['loc'] + '\n')
        
        print(f"✅ Text sitemap created: {sitemap_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating text sitemap: {e}")
        return False

def update_robots_txt(urls):
    """Update robots.txt with sitemap references."""
    print("🤖 Updating robots.txt...")
    
    robots_path = os.path.join(PROJECT_ROOT, 'robots.txt')
    
    # Read existing robots.txt
    existing_content = ""
    if os.path.exists(robots_path):
        try:
            with open(robots_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except:
            pass
    
    # Remove existing sitemap lines
    lines = existing_content.split('\n')
    filtered_lines = [line for line in lines if not line.strip().startswith('Sitemap:')]
    
    # Add new sitemap references
    filtered_lines.append('')
    filtered_lines.append('# Sitemaps')
    filtered_lines.append(f'Sitemap: {BASE_URL}/sitemap.xml')
    filtered_lines.append(f'Sitemap: {BASE_URL}/sitemap.txt')
    
    try:
        with open(robots_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(filtered_lines))
        
        print(f"✅ Updated robots.txt")
        return True
        
    except Exception as e:
        print(f"❌ Error updating robots.txt: {e}")
        return False

def create_github_workflow():
    """Create GitHub workflow to automatically update sitemaps."""
    print("⚙️ Creating GitHub workflow...")
    
    workflow_dir = os.path.join(PROJECT_ROOT, '.github', 'workflows')
    workflow_path = os.path.join(workflow_dir, 'update_sitemap.yml')
    
    # Create directory if it doesn't exist
    os.makedirs(workflow_dir, exist_ok=True)
    
    workflow_content = '''name: Update Sitemap

on:
  push:
    branches: [ main ]
    paths:
      - 'articles/**'
      - 'category/**'
      - 'pages/**'
      - 'json/**'
  schedule:
    # Run daily at 2 AM UTC
    - cron: '0 2 * * *'
  workflow_dispatch:

jobs:
  update-sitemap:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'
        
    - name: Generate sitemaps
      run: |
        cd python
        python sitemap_ultimate_generator.py
        
    - name: Commit and push if changed
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add sitemap.xml sitemap.txt robots.txt
        git diff --staged --quiet || git commit -m "Auto-update sitemaps [skip ci]"
        git push
'''
    
    try:
        with open(workflow_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(workflow_content)
        
        print(f"✅ Created GitHub workflow: {workflow_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        return False

def validate_sitemaps():
    """Validate generated sitemaps."""
    print("🔍 Validating sitemaps...")
    
    xml_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    txt_path = os.path.join(PROJECT_ROOT, 'sitemap.txt')
    
    results = {'xml': False, 'txt': False}
    
    # Validate XML sitemap
    if os.path.exists(xml_path):
        try:
            with open(xml_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            checks = [
                content.startswith('<?xml'),
                'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' in content,
                '<urlset>' in content and '</urlset>' in content,
                content.count('<loc>') > 0
            ]
            
            if all(checks):
                results['xml'] = True
                print(f"✅ XML sitemap validation passed")
            else:
                print(f"❌ XML sitemap validation failed")
                
        except Exception as e:
            print(f"❌ XML sitemap validation error: {e}")
    
    # Validate text sitemap
    if os.path.exists(txt_path):
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) > 0 and all(line.strip().startswith('http') for line in lines if line.strip()):
                results['txt'] = True
                print(f"✅ Text sitemap validation passed")
            else:
                print(f"❌ Text sitemap validation failed")
                
        except Exception as e:
            print(f"❌ Text sitemap validation error: {e}")
    
    return results

def main():
    """Main function."""
    print("🚀 Ultimate Sitemap Generator for GitHub Pages")
    print("=" * 60)
    
    # Collect all URLs
    urls = collect_all_urls()
    
    if not urls:
        print("❌ No URLs found!")
        return 1
    
    print("\n" + "=" * 60)
    
    # Generate sitemaps
    xml_success = generate_xml_sitemap(urls)
    txt_success = generate_txt_sitemap(urls)
    
    print("\n" + "=" * 60)
    
    # Update robots.txt
    update_robots_txt(urls)
    
    print("\n" + "=" * 60)
    
    # Create GitHub workflow
    create_github_workflow()
    
    print("\n" + "=" * 60)
    
    # Validate sitemaps
    validation_results = validate_sitemaps()
    
    print("\n" + "=" * 60)
    print("📋 NEXT STEPS:")
    print("1. Commit and push ALL files to GitHub:")
    print("   - sitemap.xml")
    print("   - sitemap.txt") 
    print("   - robots.txt")
    print("   - .github/workflows/update_sitemap.yml")
    print()
    print("2. Wait 5-10 minutes for GitHub Pages to deploy")
    print()
    print("3. Test sitemap accessibility:")
    print(f"   - {BASE_URL}/sitemap.xml")
    print(f"   - {BASE_URL}/sitemap.txt")
    print()
    print("4. Submit to Google Search Console:")
    print("   - Try sitemap.xml first")
    print("   - If XML fails, try sitemap.txt")
    print()
    print("5. Use Google's URL Inspection tool to test individual URLs")
    print()
    print("🔧 TROUBLESHOOTING:")
    print("- Clear browser cache before testing")
    print("- Use incognito/private mode")
    print("- Test with curl: curl -I https://omnitrends.github.io/sitemap.xml")
    print("- Check GitHub Pages deployment status")
    print("- Wait 24-48 hours for Google to process")
    
    if xml_success and txt_success:
        print("\n✅ All sitemaps generated successfully!")
        return 0
    else:
        print("\n⚠️  Some sitemaps failed to generate")
        return 1

if __name__ == "__main__":
    exit(main())