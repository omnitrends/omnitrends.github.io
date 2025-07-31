#!/usr/bin/env python3
"""
GitHub Pages Compatible Sitemap Generator for OmniTrends

This generator creates a sitemap.xml that works properly with GitHub Pages
and Google Search Console, addressing common serving and parsing issues.
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
    """Format date for sitemap (W3C Datetime format)."""
    if date_string:
        try:
            # Parse "31 July 2025" format
            parsed_date = datetime.strptime(date_string.strip(), '%d %B %Y')
            # Return in W3C format with timezone
            return parsed_date.strftime('%Y-%m-%dT12:00:00+00:00')
        except:
            pass
    
    # Return current date in W3C format
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')

def get_file_date(file_path):
    """Get file modification date in W3C format."""
    try:
        if os.path.exists(file_path):
            timestamp = os.path.getmtime(file_path)
            return datetime.fromtimestamp(timestamp, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')
    except:
        pass
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S+00:00')

def escape_xml(text):
    """Escape special XML characters."""
    if not text:
        return text
    
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text

def generate_sitemap():
    """Generate XML sitemap with proper formatting for GitHub Pages."""
    print("🗺️  Generating GitHub Pages compatible sitemap...")
    
    # Load data
    articles = load_json_data('articles.json')
    categories_data = load_json_data('categories.json')
    categories = categories_data.get('categories', []) if isinstance(categories_data, dict) else []
    
    print(f"📄 Found {len(articles)} articles and {len(categories)} categories")
    
    # Build sitemap content
    sitemap_content = []
    
    # XML declaration and root element
    sitemap_content.append('<?xml version="1.0" encoding="UTF-8"?>')
    sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # 1. Homepage
    index_date = get_file_date(os.path.join(PROJECT_ROOT, 'index.html'))
    sitemap_content.extend([
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
            sitemap_content.extend([
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
                sitemap_content.extend([
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
                
                sitemap_content.extend([
                    '  <url>',
                    f'    <loc>{BASE_URL}/{article_path}</loc>',
                    f'    <lastmod>{article_date}</lastmod>',
                    '    <changefreq>monthly</changefreq>',
                    f'    <priority>{priority}</priority>',
                    '  </url>'
                ])
    
    # Close sitemap
    sitemap_content.append('</urlset>')
    
    # Write sitemap with proper encoding
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    try:
        # Write with explicit UTF-8 BOM to ensure proper encoding recognition
        with open(sitemap_path, 'w', encoding='utf-8-sig', newline='\n') as f:
            f.write('\n'.join(sitemap_content))
        
        print(f"✅ Sitemap generated successfully!")
        print(f"📍 Location: {sitemap_path}")
        print(f"📊 Total URLs: {len([line for line in sitemap_content if '<loc>' in line])}")
        
        # Show file size
        file_size = os.path.getsize(sitemap_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing sitemap: {e}")
        return False

def create_htaccess():
    """Create .htaccess file to ensure proper MIME type for XML files."""
    htaccess_path = os.path.join(PROJECT_ROOT, '.htaccess')
    
    htaccess_content = """# Force XML files to be served with correct MIME type
<Files "sitemap.xml">
    ForceType application/xml
</Files>

# Set proper headers for XML files
<FilesMatch "\\.xml$">
    Header set Content-Type "application/xml; charset=utf-8"
</FilesMatch>
"""
    
    try:
        with open(htaccess_path, 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
        print(f"✅ Created .htaccess file for proper XML serving")
        return True
    except Exception as e:
        print(f"⚠️  Could not create .htaccess: {e}")
        return False

def test_sitemap_accessibility():
    """Test if sitemap is accessible and properly formatted."""
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    
    if not os.path.exists(sitemap_path):
        print("❌ Sitemap file not found")
        return False
    
    try:
        with open(sitemap_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Basic validation checks
        checks = [
            ('XML Declaration', content.startswith('<?xml')),
            ('Proper Namespace', 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"' in content),
            ('Valid Structure', '<urlset>' in content and '</urlset>' in content),
            ('Has URLs', '<loc>' in content),
            ('Proper Encoding', 'encoding="UTF-8"' in content)
        ]
        
        print("\n🔍 Sitemap Validation Results:")
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        url_count = content.count('<loc>')
        print(f"\n📊 Total URLs found: {url_count}")
        
        if all_passed:
            print("✅ All validation checks passed!")
        else:
            print("⚠️  Some validation checks failed")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 OmniTrends GitHub Pages Sitemap Generator")
    print("=" * 50)
    
    success = generate_sitemap()
    
    if success:
        print("\n" + "=" * 50)
        print("🔧 Creating .htaccess for proper XML serving...")
        create_htaccess()
        
        print("\n" + "=" * 50)
        print("🔍 Testing sitemap...")
        test_sitemap_accessibility()
        
        print("\n" + "=" * 50)
        print("📋 Next Steps:")
        print("1. Commit and push both sitemap.xml and .htaccess to GitHub")
        print("2. Wait 5-10 minutes for GitHub Pages to deploy")
        print("3. Test sitemap URL: https://omnitrends.github.io/sitemap.xml")
        print("4. Verify XML is properly displayed (no script tags)")
        print("5. Resubmit to Google Search Console")
        print("6. Use 'Test live URL' in Search Console to verify")
        
        print("\n🔧 Troubleshooting Tips:")
        print("- If you still see script tags, clear browser cache")
        print("- Try accessing sitemap in incognito/private mode")
        print("- Use curl to test: curl -H 'User-Agent: Googlebot' https://omnitrends.github.io/sitemap.xml")
        print("- Check GitHub Pages deployment status in repository settings")
        
    else:
        print("❌ Sitemap generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())