#!/usr/bin/env python3
"""
HTML Sitemap Generator for OmniTrends

Creates an HTML sitemap page that's user-friendly and search engine friendly.
This can serve as both a user navigation aid and a sitemap for search engines.
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

def generate_html_sitemap():
    """Generate HTML sitemap page."""
    print("🌐 Generating HTML sitemap page...")
    
    # Load data
    articles = load_json_data('articles.json')
    categories_data = load_json_data('categories.json')
    categories = categories_data.get('categories', []) if isinstance(categories_data, dict) else []
    
    print(f"📄 Found {len(articles)} articles and {len(categories)} categories")
    
    # Group articles by category
    articles_by_category = {}
    for article in articles:
        category = article.get('category', 'Uncategorized')
        if category not in articles_by_category:
            articles_by_category[category] = []
        articles_by_category[category].append(article)
    
    # Generate HTML content
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Complete sitemap of OmniTrends website - Find all articles, categories, and pages in one place.">
    <meta name="keywords" content="sitemap, OmniTrends, articles, categories, navigation">
    <meta name="robots" content="index, follow">
    <title>Sitemap | OmniTrends</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="favicon.ico">
    
    <!-- CSS -->
    <link rel="stylesheet" href="css/style.css">
    
    <style>
        .sitemap-container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        .sitemap-header {{
            text-align: center;
            margin-bottom: 3rem;
        }}
        
        .sitemap-section {{
            margin-bottom: 3rem;
        }}
        
        .sitemap-section h2 {{
            color: #2563eb;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 0.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .sitemap-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }}
        
        .sitemap-category {{
            background: #f9fafb;
            border-radius: 8px;
            padding: 1.5rem;
        }}
        
        .sitemap-category h3 {{
            color: #1f2937;
            margin-bottom: 1rem;
        }}
        
        .sitemap-links {{
            list-style: none;
            padding: 0;
        }}
        
        .sitemap-links li {{
            margin-bottom: 0.5rem;
        }}
        
        .sitemap-links a {{
            color: #4f46e5;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .sitemap-links a:hover {{
            color: #3730a3;
            text-decoration: underline;
        }}
        
        .main-pages {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
        }}
        
        .page-link {{
            display: block;
            padding: 1rem;
            background: #f3f4f6;
            border-radius: 6px;
            text-decoration: none;
            color: #374151;
            text-align: center;
            transition: background-color 0.2s;
        }}
        
        .page-link:hover {{
            background: #e5e7eb;
        }}
        
        .stats {{
            background: #eff6ff;
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 2rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
        }}
        
        .stat-item {{
            text-align: center;
        }}
        
        .stat-number {{
            font-size: 2rem;
            font-weight: bold;
            color: #2563eb;
        }}
        
        .stat-label {{
            color: #6b7280;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <div class="nav__brand">
                <a href="index.html" class="nav__logo">
                    <h1>OmniTrends</h1>
                </a>
            </div>
            
            <div class="nav__menu" id="nav-menu">
                <ul class="nav__list">
                    <li class="nav__item">
                        <a href="index.html" class="nav__link">Home</a>
                    </li>
                    <li class="nav__item nav__dropdown">
                        <a href="#" class="nav__link nav__dropdown-toggle">Categories <span class="nav__arrow">▼</span></a>
                        <ul class="nav__dropdown-menu">
                            <li><a href="category/technology.html" class="nav__dropdown-link">Technology</a></li>
                            <li><a href="category/lifestyle.html" class="nav__dropdown-link">Lifestyle</a></li>
                            <li><a href="category/business.html" class="nav__dropdown-link">Business</a></li>
                            <li><a href="category/innovation.html" class="nav__dropdown-link">Innovation</a></li>
                            <li><a href="category/news.html" class="nav__dropdown-link">News</a></li>
                            <li><a href="category/health.html" class="nav__dropdown-link">Health</a></li>
                            <li><a href="category/entertainment.html" class="nav__dropdown-link">Entertainment</a></li>
                            <li><a href="category/finance.html" class="nav__dropdown-link">Finance</a></li>
                            <li><a href="category/science.html" class="nav__dropdown-link">Science</a></li>
                            <li><a href="category/travel.html" class="nav__dropdown-link">Travel</a></li>
                            <li><a href="category/food.html" class="nav__dropdown-link">Food</a></li>
                            <li><a href="category/sports.html" class="nav__dropdown-link">Sports</a></li>
                        </ul>
                    </li>
                    <li class="nav__item nav__dropdown">
                        <a href="#" class="nav__link nav__dropdown-toggle">Pages <span class="nav__arrow">▼</span></a>
                        <ul class="nav__dropdown-menu">
                            <li><a href="pages/about.html" class="nav__dropdown-link">About</a></li>
                            <li><a href="pages/contact.html" class="nav__dropdown-link">Contact</a></li>
                            <li><a href="pages/privacy.html" class="nav__dropdown-link">Privacy Policy</a></li>
                            <li><a href="pages/terms.html" class="nav__dropdown-link">Terms & Conditions</a></li>
                            <li><a href="pages/disclaimer.html" class="nav__dropdown-link">Disclaimer</a></li>
                        </ul>
                    </li>
                </ul>
            </div>
            
            <div class="nav__toggle" id="nav-toggle">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </nav>
    </header>

    <main class="sitemap-container">
        <div class="sitemap-header">
            <h1>Website Sitemap</h1>
            <p>Complete navigation guide to all content on OmniTrends</p>
            <p><small>Last updated: {datetime.now().strftime('%B %d, %Y')}</small></p>
        </div>

        <div class="stats">
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-number">{len(articles)}</div>
                    <div class="stat-label">Articles</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{len(categories)}</div>
                    <div class="stat-label">Categories</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">5</div>
                    <div class="stat-label">Main Pages</div>
                </div>
            </div>
        </div>

        <div class="sitemap-section">
            <h2>Main Pages</h2>
            <div class="main-pages">
                <a href="index.html" class="page-link">Home</a>
                <a href="pages/about.html" class="page-link">About</a>
                <a href="pages/contact.html" class="page-link">Contact</a>
                <a href="pages/privacy.html" class="page-link">Privacy Policy</a>
                <a href="pages/terms.html" class="page-link">Terms & Conditions</a>
                <a href="pages/disclaimer.html" class="page-link">Disclaimer</a>
            </div>
        </div>

        <div class="sitemap-section">
            <h2>Categories</h2>
            <div class="main-pages">'''
    
    # Add category links
    for category in categories:
        category_slug = category.get('slug', '').lower()
        category_name = category.get('name', '')
        if category_slug:
            html_content += f'''
                <a href="category/{category_slug}.html" class="page-link">{category_name}</a>'''
    
    html_content += '''
            </div>
        </div>

        <div class="sitemap-section">
            <h2>Articles by Category</h2>
            <div class="sitemap-grid">'''
    
    # Add articles grouped by category
    for category_name, category_articles in articles_by_category.items():
        html_content += f'''
                <div class="sitemap-category">
                    <h3>{category_name} ({len(category_articles)} articles)</h3>
                    <ul class="sitemap-links">'''
        
        # Sort articles by date (newest first)
        sorted_articles = sorted(category_articles, 
                               key=lambda x: datetime.strptime(x.get('date', '01 January 2000'), '%d %B %Y'), 
                               reverse=True)
        
        for article in sorted_articles:
            article_id = article.get('id', '')
            article_title = article.get('title', '')
            article_date = article.get('date', '')
            
            if article_id and article_title:
                html_content += f'''
                        <li>
                            <a href="articles/{article_id}.html" title="{article_title}">
                                {article_title}
                            </a>
                            <small style="color: #6b7280; display: block; margin-top: 0.25rem;">
                                {article_date}
                            </small>
                        </li>'''
        
        html_content += '''
                    </ul>
                </div>'''
    
    html_content += '''
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer__content">
                <div class="footer__section">
                    <h3 class="footer__title">OmniTrends</h3>
                    <p class="footer__description">Your source for the latest trends, insights, and discoveries across technology, lifestyle, and innovation.</p>
                </div>
                
                <div class="footer__section">
                    <h4 class="footer__subtitle">Quick Links</h4>
                    <ul class="footer__links">
                        <li><a href="index.html">Home</a></li>
                        <li><a href="pages/about.html">About</a></li>
                        <li><a href="pages/contact.html">Contact</a></li>
                        <li><a href="sitemap.html">Sitemap</a></li>
                    </ul>
                </div>
                
                <div class="footer__section">
                    <h4 class="footer__subtitle">Legal</h4>
                    <ul class="footer__links">
                        <li><a href="pages/privacy.html">Privacy Policy</a></li>
                        <li><a href="pages/terms.html">Terms & Conditions</a></li>
                        <li><a href="pages/disclaimer.html">Disclaimer</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer__bottom">
                <p>&copy; 2025 OmniTrends. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="js/main.js"></script>
</body>
</html>'''
    
    # Write HTML sitemap
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.html')
    
    try:
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ HTML sitemap generated successfully!")
        print(f"📍 Location: {sitemap_path}")
        print(f"📊 Total articles: {len(articles)}")
        print(f"📊 Total categories: {len(categories)}")
        
        # Show file size
        file_size = os.path.getsize(sitemap_path)
        print(f"📁 File size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing sitemap: {e}")
        return False

def main():
    """Main function."""
    print("🚀 OmniTrends HTML Sitemap Generator")
    print("=" * 40)
    
    success = generate_html_sitemap()
    
    if success:
        print("\n" + "=" * 40)
        print("📋 Next Steps:")
        print("1. Commit and push sitemap.html to GitHub")
        print("2. Add link to sitemap.html in your footer/navigation")
        print("3. Submit sitemap.html to Google Search Console")
        print("4. URL: https://omnitrends.github.io/sitemap.html")
        print("5. This provides both user and SEO benefits!")
    else:
        print("❌ HTML sitemap generation failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())