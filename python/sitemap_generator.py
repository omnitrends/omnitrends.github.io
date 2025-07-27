#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sitemap and Robots.txt Generator for OmniTrends
Generates sitemap.xml and robots.txt files optimized for Google AdSense
"""

import os
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

# Fix Unicode output issues on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


class SitemapGenerator:
    def __init__(self, base_url="https://omnitrends.github.io", root_dir=None):
        self.base_url = base_url.rstrip('/')
        if root_dir is None:
            # Get the parent directory of the script (go up from python/ to root)
            self.root_dir = Path(__file__).parent.parent
        else:
            self.root_dir = Path(root_dir)
        
        self.sitemap_urls = []
        
    def add_url(self, loc, lastmod=None, changefreq="monthly", priority="0.5"):
        """Add a URL to the sitemap"""
        url_data = {
            'loc': f"{self.base_url}/{loc.lstrip('/')}",
            'lastmod': lastmod or datetime.now().strftime('%Y-%m-%d'),
            'changefreq': changefreq,
            'priority': priority
        }
        self.sitemap_urls.append(url_data)
    
    def scan_html_files(self):
        """Scan for HTML files in the website structure"""
        # Add main pages with high priority
        main_pages = [
            ('', 'daily', '1.0'),  # Homepage
            ('pages/about.html', 'monthly', '0.8'),
            ('pages/contact.html', 'monthly', '0.7'),
            ('pages/privacy.html', 'yearly', '0.3'),
            ('pages/terms.html', 'yearly', '0.3'),
            ('pages/disclaimer.html', 'yearly', '0.3'),
        ]
        
        for page, changefreq, priority in main_pages:
            if not page or (self.root_dir / page).exists() or page == '':
                self.add_url(page, changefreq=changefreq, priority=priority)
        
        # Add category pages
        category_dir = self.root_dir / 'category'
        if category_dir.exists():
            for category_file in category_dir.glob('*.html'):
                self.add_url(f'category/{category_file.name}', 
                           changefreq='weekly', priority='0.7')
    
    def scan_articles(self):
        """Scan articles from JSON file"""
        articles_json = self.root_dir / 'json' / 'articles.json'
        if articles_json.exists():
            try:
                with open(articles_json, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                
                for article in articles:
                    # Convert date to ISO format for lastmod
                    try:
                        article_date = datetime.strptime(article['date'], '%d %B %Y')
                        lastmod = article_date.strftime('%Y-%m-%d')
                    except:
                        lastmod = datetime.now().strftime('%Y-%m-%d')
                    
                    # Higher priority for featured articles
                    priority = '0.9' if article.get('featured', False) else '0.8'
                    
                    self.add_url(article['url'], 
                               lastmod=lastmod,
                               changefreq='monthly', 
                               priority=priority)
            except Exception as e:
                print(f"Error reading articles.json: {e}")
    
    def generate_sitemap_xml(self):
        """Generate sitemap.xml file"""
        # Create XML structure
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        urlset.set('xmlns:image', 'http://www.google.com/schemas/sitemap-image/1.1')
        
        for url_data in self.sitemap_urls:
            url_elem = ET.SubElement(urlset, 'url')
            
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = url_data['loc']
            
            lastmod_elem = ET.SubElement(url_elem, 'lastmod')
            lastmod_elem.text = url_data['lastmod']
            
            changefreq_elem = ET.SubElement(url_elem, 'changefreq')
            changefreq_elem.text = url_data['changefreq']
            
            priority_elem = ET.SubElement(url_elem, 'priority')
            priority_elem.text = url_data['priority']
        
        # Create the tree and write to file
        tree = ET.ElementTree(urlset)
        ET.indent(tree, space="  ", level=0)
        
        sitemap_path = self.root_dir / 'sitemap.xml'
        with open(sitemap_path, 'wb') as f:
            tree.write(f, encoding='utf-8', xml_declaration=True)
        
        print(f"[SUCCESS] Sitemap generated: {sitemap_path}")
        print(f"  Total URLs: {len(self.sitemap_urls)}")
    
    def generate_robots_txt(self):
        """Generate robots.txt file optimized for Google AdSense"""
        robots_content = f"""# Robots.txt for OmniTrends - Google AdSense Optimized

# Allow all web crawlers access to all content
User-agent: *
Allow: /

# Specifically allow Google bots (important for AdSense)
User-agent: Googlebot
Allow: /

User-agent: Googlebot-Image
Allow: /

User-agent: Googlebot-News
Allow: /

User-agent: AdsBot-Google
Allow: /

User-agent: AdsBot-Google-Mobile
Allow: /

# Allow social media crawlers
User-agent: facebookexternalhit
Allow: /

User-agent: Twitterbot
Allow: /

# Block access to sensitive directories
Disallow: /.git/
Disallow: /.venv/
Disallow: /temp/
Disallow: /.zencoder/

# Allow access to all other directories important for AdSense
Allow: /css/
Allow: /js/
Allow: /images/
Allow: /json/
Allow: /articles/
Allow: /category/
Allow: /pages/

# Sitemap location
Sitemap: {self.base_url}/sitemap.xml

# Crawl delay (optional, helps with server load)
Crawl-delay: 1
"""
        
        robots_path = self.root_dir / 'robots.txt'
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write(robots_content)
        
        print(f"[SUCCESS] Robots.txt generated: {robots_path}")
    
    def generate_all(self):
        """Generate both sitemap.xml and robots.txt"""
        print("[STARTING] Starting sitemap and robots.txt generation...")
        print(f"   Base URL: {self.base_url}")
        print(f"   Root directory: {self.root_dir}")
        
        # Clear existing URLs
        self.sitemap_urls = []
        
        # Scan and add URLs
        print("\n[SCANNING] Scanning website structure...")
        self.scan_html_files()
        self.scan_articles()
        
        # Sort URLs by priority (highest first)
        self.sitemap_urls.sort(key=lambda x: float(x['priority']), reverse=True)
        
        # Generate files
        print("\n[GENERATING] Generating files...")
        self.generate_sitemap_xml()
        self.generate_robots_txt()
        
        print("\n[COMPLETE] Generation complete!")
        print(f"   Sitemap: {self.base_url}/sitemap.xml")
        print(f"   Robots: {self.base_url}/robots.txt")


def main():
    """Main function to run the generator"""
    generator = SitemapGenerator()
    generator.generate_all()


if __name__ == "__main__":
    main()