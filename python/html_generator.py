import json
import os
import shutil
from datetime import datetime
import markdown
from PIL import Image

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def read_id_from_keyword_selection():
    """Read the id value from temp/keyword_selection.json"""
    keyword_selection_path = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
    try:
        with open(keyword_selection_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('id')
    except FileNotFoundError:
        print(f"Error: {keyword_selection_path} not found")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in keyword_selection.json")
        return None

def resize_final_image():
    """Resize temp/final.jpg to 1200x630px and save it with the same name in the same location"""
    image_path = os.path.join(PROJECT_ROOT, 'temp', 'final.jpg')
    
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Resize to 1200x630px
            resized_img = img.resize((1200, 630), Image.Resampling.LANCZOS)
            
            # Save the resized image with the same name and location
            resized_img.save(image_path, 'JPEG', quality=95)
            print(f"Successfully resized {image_path} to 1200x630px")
            
    except FileNotFoundError:
        print(f"Error: {image_path} not found")
    except Exception as e:
        print(f"Error resizing image: {str(e)}")

def rename_final_md_to_id(article_id):
    """Rename temp/final.md to temp/{id}.md"""
    if not article_id:
        print("Error: No article ID provided")
        return False
    
    source_path = os.path.join(PROJECT_ROOT, 'temp', 'final.md')
    target_path = os.path.join(PROJECT_ROOT, 'temp', f'{article_id}.md')
    
    try:
        if os.path.exists(source_path):
            shutil.move(source_path, target_path)
            print(f"Renamed final.md to {article_id}.md")
            return True
        else:
            print("Error: temp/final.md not found")
            return False
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False

def generate_html_from_markdown(article_id):
    """Generate HTML file from temp/{id}.md and save to articles/{id}.html"""
    if not article_id:
        print("Error: No article ID provided")
        return False
    
    # Read the keyword selection data
    keyword_selection_path = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
    try:
        with open(keyword_selection_path, 'r', encoding='utf-8') as f:
            article_data = json.load(f)
    except Exception as e:
        print(f"Error reading keyword_selection.json: {e}")
        return False
    
    # Read the markdown content
    md_path = os.path.join(PROJECT_ROOT, 'temp', f'{article_id}.md')
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        print(f"Error reading markdown file: {e}")
        return False
    
    # Convert markdown to HTML
    md = markdown.Markdown()
    html_content = md.convert(md_content)
    
    # Extract keywords for meta tags
    keywords = article_data.get('keyword', '').split()
    keywords_str = ', '.join(keywords[:4])  # Limit to 4 keywords
    
    # Generate the complete HTML
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <meta name="description" content="{article_data.get('excerpt', '')}">
    <meta name="keywords" content="{keywords_str}">
    <meta name="author" content="OmniTrends">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <meta name="theme-color" content="#2563eb">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="{article_data.get('title', '')} - OmniTrends">
    <meta name="format-detection" content="telephone=no">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://omnitrends.github.io/articles/{article_id}.html">
    <meta property="og:title" content="{article_data.get('title', '')}">
    <meta property="og:description" content="{article_data.get('excerpt', '')}">
    <meta property="og:image" content="https://omnitrends.github.io/images/{article_id}.webp">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://omnitrends.github.io/articles/{article_id}.html">
    <meta property="twitter:title" content="{article_data.get('title', '')}">
    <meta property="twitter:description" content="{article_data.get('excerpt', '')}">
    <meta property="twitter:image" content="https://omnitrends.github.io/images/{article_id}.webp">
    
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
    
    <title>{article_data.get('title', '')} | OmniTrends</title>
    
    <!-- JSON-LD Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "{article_data.get('title', '')}",
        "description": "{article_data.get('excerpt', '')}",
        "image": "https://omnitrends.github.io/images/{article_id}.webp",
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
        "datePublished": "{article_data.get('date', datetime.now().strftime('%Y-%m-%d'))}",
        "dateModified": "{article_data.get('date', datetime.now().strftime('%Y-%m-%d'))}",
        "mainEntityOfPage": {{
            "@type": "WebPage",
            "@id": "https://omnitrends.github.io/articles/{article_id}.html"
        }},
        "articleSection": "{article_data.get('category', '')}"
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
                    <a href="../category/{article_data.get('category', '').lower()}.html" class="article-category">{article_data.get('category', '')}</a>
                    <span class="article-date" id="article-date">{article_data.get('date', '')}</span>
                </div>
                <h1 class="article-title">{article_data.get('title', '')}</h1>
                <p class="article-description">{article_data.get('excerpt', '')}</p>
            </div>
        </div>
    </section>

    <!-- Article Content -->
    <main class="article-content">
        <div class="container">
            <article class="article">
                <div class="article__image">
                    <img src="../images/{article_id}.webp" alt="{article_data.get('title', '')}" loading="lazy">
                </div>
                
                <div class="article__body">
                    {html_content}
                </div>

                <div class="article__footer">
                    <div class="article__tags">
                        <span class="tag">{article_data.get('category', '')}</span>
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
        // Update the article date display
        document.addEventListener('DOMContentLoaded', function() {{
            const articleDate = document.getElementById('article-date');
            if (articleDate) {{
                const date = new Date('{article_data.get('date', '')}');
                const options = {{ year: 'numeric', month: 'long', day: 'numeric' }};
                articleDate.textContent = date.toLocaleDateString('en-US', options);
            }}
        }});
    </script>
</body>
</html>'''
    
    # Ensure articles directory exists
    articles_dir = os.path.join(PROJECT_ROOT, 'articles')
    os.makedirs(articles_dir, exist_ok=True)
    
    # Save the HTML file
    html_path = os.path.join(PROJECT_ROOT, 'articles', f'{article_id}.html')
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_template)
        print(f"Generated HTML file: {article_id}.html")
        return True
    except Exception as e:
        print(f"Error writing HTML file: {e}")
        return False

def process_image_files(article_id):
    """Rename temp/final.jpg to temp/{id}.jpg, convert to webp, and copy to images/"""
    if not article_id:
        print("Error: No article ID provided")
        return False
    
    # Step 1: Rename temp/final.jpg to temp/{id}.jpg
    source_jpg = os.path.join(PROJECT_ROOT, 'temp', 'final.jpg')
    temp_jpg = os.path.join(PROJECT_ROOT, 'temp', f'{article_id}.jpg')
    
    try:
        if os.path.exists(source_jpg):
            shutil.move(source_jpg, temp_jpg)
            print(f"Renamed final.jpg to {article_id}.jpg")
        else:
            print("Error: temp/final.jpg not found")
            return False
    except Exception as e:
        print(f"Error renaming JPG file: {e}")
        return False
    
    # Step 2: Convert temp/{id}.jpg to temp/{id}.webp
    temp_webp = os.path.join(PROJECT_ROOT, 'temp', f'{article_id}.webp')
    
    try:
        with Image.open(temp_jpg) as img:
            # Convert to RGB if necessary (for JPEG compatibility)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Save as WebP with high quality
            img.save(temp_webp, 'WEBP', quality=85, optimize=True)
            print(f"Converted {article_id}.jpg to {article_id}.webp")
    except Exception as e:
        print(f"Error converting to WebP: {e}")
        return False
    
    # Step 3: Copy temp/{id}.webp to images/{id}.webp
    # Ensure images directory exists
    images_dir = os.path.join(PROJECT_ROOT, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    final_webp = os.path.join(PROJECT_ROOT, 'images', f'{article_id}.webp')
    
    try:
        shutil.copy2(temp_webp, final_webp)
        print(f"Copied {article_id}.webp to images folder")
        return True
    except Exception as e:
        print(f"Error copying WebP to images folder: {e}")
        return False

def update_articles_json():
    """Copy element from temp/keyword_selection.json to top of json/articles.json"""
    # Read the new article data
    keyword_selection_path = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
    try:
        with open(keyword_selection_path, 'r', encoding='utf-8') as f:
            new_article = json.load(f)
    except Exception as e:
        print(f"Error reading keyword_selection.json: {e}")
        return False
    
    # Read existing articles.json
    articles_path = os.path.join(PROJECT_ROOT, 'json', 'articles.json')
    try:
        with open(articles_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        articles = []
    except Exception as e:
        print(f"Error reading articles.json: {e}")
        return False
    
    # Check if article already exists (avoid duplicates)
    article_exists = any(article.get('id') == new_article.get('id') for article in articles)
    
    if not article_exists:
        # Add new article to the top of the list
        articles.insert(0, new_article)
        
        # Save updated articles.json
        # Ensure json directory exists
        json_dir = os.path.join(PROJECT_ROOT, 'json')
        os.makedirs(json_dir, exist_ok=True)
        
        try:
            with open(articles_path, 'w', encoding='utf-8') as f:
                json.dump(articles, f, indent=4, ensure_ascii=False)
            print("Updated articles.json with new article")
            return True
        except Exception as e:
            print(f"Error writing articles.json: {e}")
            return False
    else:
        print("Article already exists in articles.json")
        return True

def update_featured_articles():
    """Ensure only top 9 articles are featured in json/articles.json"""
    articles_path = os.path.join(PROJECT_ROOT, 'json', 'articles.json')
    
    try:
        with open(articles_path, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except Exception as e:
        print(f"Error reading articles.json: {e}")
        return False
    
    # Update featured status - only top 9 should be featured
    for i, article in enumerate(articles):
        if i < 9:
            article['featured'] = True
        else:
            article['featured'] = False
    
    # Save updated articles.json
    # Ensure json directory exists
    json_dir = os.path.join(PROJECT_ROOT, 'json')
    os.makedirs(json_dir, exist_ok=True)
    
    try:
        with open(articles_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=4, ensure_ascii=False)
        print("Updated featured articles (top 9 are now featured)")
        return True
    except Exception as e:
        print(f"Error writing articles.json: {e}")
        return False

def clear_temp_folder():
    """Clear all files from the temp folder"""
    temp_folder = os.path.join(PROJECT_ROOT, 'temp')
    
    try:
        for filename in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Removed: {filename}")
        print("Temp folder cleared successfully")
        return True
    except Exception as e:
        print(f"Error clearing temp folder: {e}")
        return False

def generate_sitemap():
    """Generate sitemap.xml for Google Search Console"""
    base_url = "https://omnitrends.github.io"
    sitemap_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add index.html
    sitemap_content.append('  <url>')
    sitemap_content.append(f'    <loc>{base_url}/index.html</loc>')
    sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap_content.append('    <changefreq>daily</changefreq>')
    sitemap_content.append('    <priority>1.0</priority>')
    sitemap_content.append('  </url>')
    
    # Add 404.html
    sitemap_content.append('  <url>')
    sitemap_content.append(f'    <loc>{base_url}/404.html</loc>')
    sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
    sitemap_content.append('    <changefreq>monthly</changefreq>')
    sitemap_content.append('    <priority>0.1</priority>')
    sitemap_content.append('  </url>')
    
    # Add pages from pages folder
    pages_folder = os.path.join(PROJECT_ROOT, 'pages')
    try:
        for filename in os.listdir(pages_folder):
            if filename.endswith('.html'):
                sitemap_content.append('  <url>')
                sitemap_content.append(f'    <loc>{base_url}/pages/{filename}</loc>')
                sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
                sitemap_content.append('    <changefreq>monthly</changefreq>')
                sitemap_content.append('    <priority>0.5</priority>')
                sitemap_content.append('  </url>')
    except Exception as e:
        print(f"Error reading pages folder: {e}")
    
    # Add articles from articles folder
    articles_folder = os.path.join(PROJECT_ROOT, 'articles')
    try:
        for filename in os.listdir(articles_folder):
            if filename.endswith('.html'):
                sitemap_content.append('  <url>')
                sitemap_content.append(f'    <loc>{base_url}/articles/{filename}</loc>')
                sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
                sitemap_content.append('    <changefreq>weekly</changefreq>')
                sitemap_content.append('    <priority>0.8</priority>')
                sitemap_content.append('  </url>')
    except Exception as e:
        print(f"Error reading articles folder: {e}")
    
    # Add category pages
    category_folder = os.path.join(PROJECT_ROOT, 'category')
    try:
        for filename in os.listdir(category_folder):
            if filename.endswith('.html'):
                sitemap_content.append('  <url>')
                sitemap_content.append(f'    <loc>{base_url}/category/{filename}</loc>')
                sitemap_content.append(f'    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>')
                sitemap_content.append('    <changefreq>weekly</changefreq>')
                sitemap_content.append('    <priority>0.6</priority>')
                sitemap_content.append('  </url>')
    except Exception as e:
        print(f"Error reading category folder: {e}")
    
    sitemap_content.append('</urlset>')
    
    # Save sitemap.xml
    sitemap_path = os.path.join(PROJECT_ROOT, 'sitemap.xml')
    try:
        with open(sitemap_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sitemap_content))
        print("Generated sitemap.xml successfully")
        return True
    except Exception as e:
        print(f"Error writing sitemap.xml: {e}")
        return False

def generate_robots_txt():
    """Generate robots.txt file"""
    robots_content = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow temp and development files",
        "Disallow: /temp/",
        "Disallow: /.venv/",
        "Disallow: /.github/",
        "Disallow: /python/",
        "",
        "# Sitemap location",
        "Sitemap: https://omnitrends.github.io/sitemap.xml"
    ]
    
    robots_path = os.path.join(PROJECT_ROOT, 'robots.txt')
    try:
        with open(robots_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(robots_content))
        print("Generated robots.txt successfully")
        return True
    except Exception as e:
        print(f"Error writing robots.txt: {e}")
        return False

def main():
    """Main function to execute all steps"""
    print("Starting HTML generation process...")
    
    # Step 1: Read ID from keyword_selection.json
    article_id = read_id_from_keyword_selection()
    if not article_id:
        print("Failed to read article ID. Exiting.")
        return False
    
    print(f"Processing article: {article_id}")
    
    # Step 2: Rename final.md to {id}.md
    if not rename_final_md_to_id(article_id):
        print("Failed to rename markdown file. Exiting.")
        return False
    
    # Step 3: Generate HTML from markdown
    if not generate_html_from_markdown(article_id):
        print("Failed to generate HTML file. Exiting.")
        return False
    
    # Step 4: Process image files
    if not process_image_files(article_id):
        print("Failed to process image files. Exiting.")
        return False
    
    # Step 5: Update articles.json
    if not update_articles_json():
        print("Failed to update articles.json. Exiting.")
        return False
    
    # Step 6: Update featured articles (only top 9)
    if not update_featured_articles():
        print("Failed to update featured articles. Exiting.")
        return False
    
    # Step 7: Generate sitemap.xml
    if not generate_sitemap():
        print("Failed to generate sitemap.xml. Exiting.")
        return False
    
    # Step 8: Generate robots.txt
    if not generate_robots_txt():
        print("Failed to generate robots.txt. Exiting.")
        return False
    
    # Step 9: Clear temp folder
    if not clear_temp_folder():
        print("Failed to clear temp folder. Exiting.")
        return False
    
    print("HTML generation process completed successfully!")
    return True

if __name__ == "__main__":
    main()