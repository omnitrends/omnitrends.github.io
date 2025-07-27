# -*- coding: utf-8 -*-
import json
import os
import shutil
import re
import sys
from datetime import datetime
from PIL import Image

# Fix Unicode output issues on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

def generate_slug(title):
    """Convert title to URL-friendly slug"""
    # Convert to lowercase
    slug = title.lower()
    # Remove special characters and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def markdown_to_html(markdown_content):
    """Convert markdown content to HTML"""
    lines = markdown_content.split('\n')
    html_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Handle headings
        if line.startswith('# '):
            continue  # Skip main title as it's handled separately
        elif line.startswith('## '):
            html_content.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_content.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html_content.append(f'<h4>{line[5:]}</h4>')
        # Handle bold text
        elif '**' in line:
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_content.append(f'<p>{line}</p>')
        # Regular paragraphs
        else:
            html_content.append(f'<p>{line}</p>')
    
    return '\n                    '.join(html_content)

def generate_html(article_data, content_html, slug):
    """Generate HTML file from template"""
    title = article_data['gemini_title']
    category = article_data['category']
    date = article_data['date']
    excerpt = article_data['excerpt']
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <meta name="description" content="{excerpt}">
    <meta name="keywords" content="{article_data['keyword']}, {category.lower()}, trends, news">
    <meta name="author" content="OmniTrends">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <meta name="theme-color" content="#2563eb">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="{title} - OmniTrends">
    <meta name="format-detection" content="telephone=no">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://omnitrends.github.io/articles/{slug}.html">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{excerpt}">
    <meta property="og:image" content="https://omnitrends.github.io/images/{slug}.webp">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://omnitrends.github.io/articles/{slug}.html">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{excerpt}">
    <meta property="twitter:image" content="https://omnitrends.github.io/images/{slug}.webp">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="../favicon.ico">
    
    <!-- Manifest -->
    <link rel="manifest" href="../json/manifest.json">
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Performance optimizations -->
    <link rel="dns-prefetch" href="//fonts.googleapis.com">
    <link rel="dns-prefetch" href="//fonts.gstatic.com">
    
    <!-- CSS -->
    <link rel="stylesheet" href="../css/style.css">
    
    <title>{title} | OmniTrends</title>
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{title}",
        "description": "{excerpt}",
        "image": "https://omnitrends.github.io/images/{slug}.webp",
        "author": {{
            "@type": "Organization",
            "name": "OmniTrends"
        }},
        "publisher": {{
            "@type": "Organization",
            "name": "OmniTrends",
            "logo": {{
                "@type": "ImageObject",
                "url": "https://omnitrends.github.io/images/logo.png"
            }}
        }},
        "datePublished": "{datetime.strptime(date, '%d %B %Y').strftime('%Y-%m-%d')}",
        "dateModified": "{datetime.strptime(date, '%d %B %Y').strftime('%Y-%m-%d')}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://omnitrends.github.io/articles/{slug}.html"
        }},
        "articleSection": "{category}"
    }}
    </script>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <nav class="nav container">
            <div class="nav__brand">
                <a href="../index.html" class="nav__logo">
                    <h1>OmniTrends</h1>
                </a>
            </div>
            
            <div class="nav__menu" id="nav-menu">
                <ul class="nav__list">
                    <li class="nav__item">
                        <a href="../index.html" class="nav__link">Home</a>
                    </li>
                    <li class="nav__item nav__dropdown">
                        <a href="#" class="nav__link nav__dropdown-toggle">Categories <span class="nav__arrow">▼</span></a>
                        <ul class="nav__dropdown-menu">
                            <li><a href="../category/technology.html" class="nav__dropdown-link">Technology</a></li>
                            <li><a href="../category/lifestyle.html" class="nav__dropdown-link">Lifestyle</a></li>
                            <li><a href="../category/business.html" class="nav__dropdown-link">Business</a></li>
                            <li><a href="../category/innovation.html" class="nav__dropdown-link">Innovation</a></li>
                            <li><a href="../category/news.html" class="nav__dropdown-link">News</a></li>
                            <li><a href="../category/health.html" class="nav__dropdown-link">Health</a></li>
                            <li><a href="../category/entertainment.html" class="nav__dropdown-link">Entertainment</a></li>
                            <li><a href="../category/finance.html" class="nav__dropdown-link">Finance</a></li>
                            <li><a href="../category/science.html" class="nav__dropdown-link">Science</a></li>
                            <li><a href="../category/travel.html" class="nav__dropdown-link">Travel</a></li>
                            <li><a href="../category/food.html" class="nav__dropdown-link">Food</a></li>
                            <li><a href="../category/sports.html" class="nav__dropdown-link">Sports</a></li>
                        </ul>
                    </li>
                    <li class="nav__item nav__dropdown">
                        <a href="#" class="nav__link nav__dropdown-toggle">Pages <span class="nav__arrow">▼</span></a>
                        <ul class="nav__dropdown-menu">
                            <li><a href="../pages/about.html" class="nav__dropdown-link">About</a></li>
                            <li><a href="../pages/contact.html" class="nav__dropdown-link">Contact</a></li>
                            <li><a href="../pages/privacy.html" class="nav__dropdown-link">Privacy Policy</a></li>
                            <li><a href="../pages/terms.html" class="nav__dropdown-link">Terms & Conditions</a></li>
                            <li><a href="../pages/disclaimer.html" class="nav__dropdown-link">Disclaimer</a></li>
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

    <!-- Article Header -->
    <section class="article-header">
        <div class="container">
            <div class="article-header__content">
                <div class="article-meta">
                    <a href="../category/{category.lower()}.html" class="article-category">{category}</a>
                    <span class="article-date" id="article-date">{date}</span>
                </div>
                <h1 class="article-title">{title}</h1>
                <p class="article-description">{excerpt}</p>
            </div>
        </div>
    </section>

    <!-- Article Content -->
    <main class="article-content">
        <div class="container">
            <article class="article">
                <div class="article__image">
                    <img src="../images/{slug}.webp" alt="{title}" loading="lazy">
                </div>
                
                <div class="article__body">
                    {content_html}
                </div>

                <div class="article__footer">
                    <div class="article__tags">
                        <span class="tag">{category}</span>
                        <span class="tag">Trends</span>
                        <span class="tag">News</span>
                    </div>
                </div>
            </article>
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
                        <li><a href="../index.html">Home</a></li>
                        <li><a href="../pages/about.html">About</a></li>
                        <li><a href="../pages/contact.html">Contact</a></li>
                        <li><a href="../pages/privacy.html">Privacy Policy</a></li>
                        <li><a href="../pages/terms.html">Terms & Conditions</a></li>
                        <li><a href="../pages/disclaimer.html">Disclaimer</a></li>
                    </ul>
                </div>
                
                <div class="footer__section">
                    <h4 class="footer__subtitle">Categories</h4>
                    <ul class="footer__links">
                        <li><a href="../category/technology.html">Technology</a></li>
                        <li><a href="../category/lifestyle.html">Lifestyle</a></li>
                        <li><a href="../category/business.html">Business</a></li>
                        <li><a href="../category/innovation.html">Innovation</a></li>
                        <li><a href="../category/news.html">News</a></li>
                        <li><a href="../category/health.html">Health</a></li>
                        <li><a href="../category/entertainment.html">Entertainment</a></li>
                        <li><a href="../category/finance.html">Finance</a></li>
                        <li><a href="../category/science.html">Science</a></li>
                        <li><a href="../category/travel.html">Travel</a></li>
                        <li><a href="../category/food.html">Food</a></li>
                        <li><a href="../category/sports.html">Sports</a></li>
                    </ul>
                </div>
            </div>
            
            <div class="footer__bottom">
                <p>&copy; 2025 OmniTrends. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="../js/articles.js"></script>
    <script src="../js/main.js"></script>
    <script>
        // Initialize article page with data from articles.json
        document.addEventListener('DOMContentLoaded', async function() {{
            // Wait for articles to load
            await loadArticlesData();
            // Initialize this specific article page
            initializeArticlePage('{slug}');
        }});
    </script>
</body>
</html>'''
    
    return html_template

def move_image(slug):
    """Convert JPG to WebP and move image from temp to images folder"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    temp_image_path = os.path.join(script_dir, "..", "temp", "final.jpg")
    target_image_path = os.path.join(script_dir, "..", "images", f"{slug}.webp")
    
    if os.path.exists(temp_image_path):
        try:
            # Ensure the images directory exists
            images_dir = os.path.dirname(target_image_path)
            os.makedirs(images_dir, exist_ok=True)
            
            # Open the JPG image
            with Image.open(temp_image_path) as img:
                # Convert and save as WebP
                img.save(target_image_path, "WEBP", quality=85, optimize=True)
            
            # Remove the original JPG file from temp
            os.remove(temp_image_path)
            
            print(f"Image converted to WebP and moved to: {target_image_path}")
            return True
        except Exception as e:
            print(f"Error converting image: {e}")
            return False
    else:
        print(f"Warning: Image not found at {temp_image_path}")
        return False

def update_articles_json(article_data, slug):
    """Update articles.json with new article entry"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    articles_json_path = os.path.join(script_dir, "..", "json", "articles.json")
    
    # Read existing articles
    with open(articles_json_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # Check if article with same ID already exists
    existing_ids = [article['id'] for article in articles]
    if slug in existing_ids:
        print(f"Article with ID '{slug}' already exists in articles.json. Skipping...")
        return
    
    # Create new article entry
    new_article = {
        "id": slug,
        "keyword": article_data['keyword'],
        "title": article_data['gemini_title'],
        "category": article_data['category'],
        "date": article_data['date'],
        "image": f"{slug}.webp",
        "url": f"articles/{slug}.html",
        "excerpt": article_data['excerpt'],
        "featured": True  # Will be updated based on position
    }
    
    # Insert at the beginning
    articles.insert(0, new_article)
    
    # Update featured status - first 9 are featured
    for i, article in enumerate(articles):
        article['featured'] = i < 9
    
    # Write back to file
    # Ensure the json directory exists
    json_dir = os.path.dirname(articles_json_path)
    os.makedirs(json_dir, exist_ok=True)
    
    with open(articles_json_path, 'w', encoding='utf-8') as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    
    print(f"Articles.json updated with new article: {slug}")

def main():
    """Main function to orchestrate the HTML generation process"""
    # File paths (relative to script's parent directory)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    analysis_json_path = os.path.join(script_dir, "..", "temp", "article_analysis.json")
    final_md_path = os.path.join(script_dir, "..", "temp", "final.md")
    
    try:
        # Step 1: Read article analysis data
        print("Reading article analysis data...")
        with open(analysis_json_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
        
        # Step 2: Read markdown content
        print("Reading markdown content...")
        with open(final_md_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Step 3: Generate slug from title
        slug = generate_slug(article_data['gemini_title'])
        print(f"Generated slug: {slug}")
        
        # Step 4: Convert markdown to HTML
        print("Converting markdown to HTML...")
        content_html = markdown_to_html(markdown_content)
        
        # Step 5: Generate HTML file
        print("Generating HTML file...")
        html_content = generate_html(article_data, content_html, slug)
        
        # Write HTML file
        html_file_path = os.path.join(script_dir, "..", "articles", f"{slug}.html")
        
        # Ensure the articles directory exists
        articles_dir = os.path.dirname(html_file_path)
        os.makedirs(articles_dir, exist_ok=True)
        
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML file created: {html_file_path}")
        
        # Step 6: Move and rename image
        print("Moving image...")
        move_image(slug)
        
        # Step 7: Update articles.json
        print("Updating articles.json...")
        update_articles_json(article_data, slug)
        
        print("\n[SUCCESS] HTML generation completed successfully!")
        print(f"[ARTICLE] Article URL: articles/{slug}.html")
        print(f"[IMAGE] Image: images/{slug}.webp")
        print(f"[JSON] JSON updated with new entry")
        
    except Exception as e:
        print(f"[ERROR] Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()