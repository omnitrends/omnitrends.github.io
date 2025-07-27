#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Article Search and Analysis Script
Uses Bing News Search with Selenium to scrape articles and Gemini for analysis.
Searches for top trending topic from latest_trends.json and scrapes top 3 Bing news results.
"""

import json
import os
import requests
from bs4 import BeautifulSoup
import time
import random
import sys

# Set stdout to be unbuffered for real-time output
sys.stdout.reconfigure(line_buffering=True)
from urllib.parse import urljoin, urlparse, quote
import re
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from PIL import Image
import io
import base64

# Fix Unicode output issues on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class ArticleSearcher:
    def __init__(self):
        """Initialize the article searcher with Gemini API and Selenium"""
        # Load environment variables
        load_dotenv()
        
        # Configure Gemini API
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Set up headers for web scraping
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Create temp directory if it doesn't exist (relative to script's parent directory)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.temp_dir = os.path.join(script_dir, "..", "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Initialize Selenium driver
        self.driver = None
    
    def setup_driver(self):
        """Setup headless Chrome driver"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Suppress Chrome logging to console
            chrome_options.add_argument("--log-level=3")  # Suppress INFO, WARNING, and ERROR
            chrome_options.add_argument("--silent")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            print("[SUCCESS] Selenium Chrome driver initialized successfully", flush=True)
            
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}", flush=True)
            raise
    
    def close_driver(self):
        """Close the Selenium driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def _load_more_bing_results(self):
        """Scroll down to load more dynamic content from Bing"""
        try:
            print("Loading more results by scrolling...", flush=True)
            initial_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Scroll down in multiple steps to trigger dynamic loading
            for i in range(5):  # Try scrolling 5 times
                # Scroll to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for content to load
                
                # Check if new content loaded
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == initial_height:
                    break  # No more content loaded
                
                initial_height = new_height
                print(f"Scrolled {i+1}/5 - New content loaded", flush=True)
            
            # Final wait for any last content
            time.sleep(2)
            print("Dynamic content loading completed", flush=True)
            
        except Exception as e:
            print(f"Error loading more results: {e}", flush=True)
            # Continue anyway

    def _matches_query(self, title, query):
        """Check if title matches query with flexible matching"""
        if not title or not query:
            return False
        
        title_lower = title.lower()
        query_lower = query.lower()
        
        # Direct match
        if query_lower in title_lower:
            return True
        
        # Split query into words and check if most words are present
        query_words = query_lower.split()
        if len(query_words) > 1:
            matches = sum(1 for word in query_words if word in title_lower)
            # Require at least 60% of query words to match
            return matches >= len(query_words) * 0.6
        
        return False

    def _extract_bing_articles_method1(self, query, max_articles):
        """Extract articles using standard news card selectors"""
        articles = []
        try:
            selectors = [".news-card", ".newsitem", ".news-item"]
            all_news_cards = []
            
            for selector in selectors:
                cards = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if cards:
                    print(f"Method 1: Found {len(cards)} articles with selector {selector}", flush=True)
                    all_news_cards.extend(cards)
                    break
            
            for i, card in enumerate(all_news_cards):
                if len(articles) >= max_articles:
                    break
                
                try:
                    # Try multiple title selectors
                    title = ""
                    title_selectors = [".title", "h3", "h4", "a[title]", ".headline"]
                    for title_sel in title_selectors:
                        try:
                            title_element = card.find_element(By.CSS_SELECTOR, title_sel)
                            title = title_element.text.strip() or title_element.get_attribute("title") or ""
                            if title:
                                break
                        except:
                            continue
                    
                    # More flexible keyword matching
                    if not title or not self._matches_query(title, query):
                        continue
                    
                    # Extract URL
                    url = ""
                    try:
                        link_element = card.find_element(By.CSS_SELECTOR, "a")
                        url = link_element.get_attribute("href")
                    except:
                        continue
                    
                    # Extract source
                    source = "Bing News"
                    source_selectors = [".source", ".attribution", ".publisher", ".cite"]
                    for source_sel in source_selectors:
                        try:
                            source_element = card.find_element(By.CSS_SELECTOR, source_sel)
                            source = source_element.text.strip()
                            if source:
                                break
                        except:
                            continue
                    
                    # Extract snippet
                    snippet = ""
                    snippet_selectors = [".snippet", ".description", ".summary", ".abstract"]
                    for snippet_sel in snippet_selectors:
                        try:
                            snippet_element = card.find_element(By.CSS_SELECTOR, snippet_sel)
                            snippet = snippet_element.text.strip()
                            if snippet:
                                break
                        except:
                            continue
                    
                    # Extract image
                    image_url = ""
                    try:
                        img_element = card.find_element(By.CSS_SELECTOR, "img")
                        image_url = img_element.get_attribute("src") or img_element.get_attribute("data-src") or ""
                    except:
                        pass
                    
                    articles.append({
                        'title': title,
                        'link': url,
                        'source': source,
                        'time': 'Recent',
                        'snippet': snippet,
                        'image_url': image_url
                    })
                    
                    print(f"[FOUND] Method 1 - Found article {len(articles)}: {title[:50]}...", flush=True)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error in method 1: {e}", flush=True)
        
        return articles

    def _extract_bing_articles_method2(self, query, max_articles):
        """Extract articles using data attributes and alternative selectors"""
        articles = []
        try:
            selectors = ["[data-module='NewsArticle']", "article", ".algocore", ".na_cnt"]
            all_items = []
            
            for selector in selectors:
                items = self.driver.find_elements(By.CSS_SELECTOR, selector)
                if items:
                    print(f"Method 2: Found {len(items)} articles with selector {selector}", flush=True)
                    all_items.extend(items)
                    if len(all_items) > 20:  # Don't get too many
                        break
                        
            for i, item in enumerate(all_items[:max_articles * 3]):  # Search more than needed
                if len(articles) >= max_articles:
                    break
                
                try:
                    # Find title and link
                    title = ""
                    url = ""
                    
                    # Try to find clickable title link
                    title_links = item.find_elements(By.CSS_SELECTOR, "a")
                    for link in title_links:
                        title_text = link.text.strip() or link.get_attribute("title") or ""
                        link_url = link.get_attribute("href") or ""
                        
                        if title_text and link_url and self._matches_query(title_text, query):
                            title = title_text
                            url = link_url
                            break
                    
                    if not title or not url:
                        continue
                    
                    # Extract image
                    image_url = ""
                    try:
                        img_element = item.find_element(By.CSS_SELECTOR, "img")
                        image_url = img_element.get_attribute("src") or img_element.get_attribute("data-src") or ""
                    except:
                        pass
                    
                    articles.append({
                        'title': title,
                        'link': url,
                        'source': 'Bing News',
                        'time': 'Recent',
                        'snippet': '',
                        'image_url': image_url
                    })
                    
                    print(f"[FOUND] Method 2 - Found article {len(articles)}: {title[:50]}...", flush=True)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error in method 2: {e}", flush=True)
        
        return articles

    def _extract_bing_articles_fallback(self, query, max_articles):
        """Fallback method - extract any links that might be articles"""
        articles = []
        try:
            print("Method 3: Using fallback approach - searching all links...", flush=True)
            
            # Get all links on the page
            all_links = self.driver.find_elements(By.CSS_SELECTOR, "a")
            print(f"Method 3: Found {len(all_links)} total links on page", flush=True)
            
            for link in all_links:
                if len(articles) >= max_articles:
                    break
                
                try:
                    title = link.text.strip() or link.get_attribute("title") or ""
                    url = link.get_attribute("href") or ""
                    
                    # Filter for news-like URLs and titles containing query
                    if (title and url and 
                        self._matches_query(title, query) and
                        len(title) > 20 and  # Reasonable title length
                        any(domain in url.lower() for domain in ['news', 'article', 'story', '.com', '.in']) and
                        not any(skip in url.lower() for skip in ['javascript:', 'mailto:', '#', 'bing.com/search'])):
                        
                        articles.append({
                            'title': title,
                            'link': url,
                            'source': 'Web Search',
                            'time': 'Recent',
                            'snippet': '',
                            'image_url': ''
                        })
                        
                        print(f"[FOUND] Method 3 - Found article {len(articles)}: {title[:50]}...", flush=True)
                        
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"Error in method 3: {e}", flush=True)
        
        return articles
    
    def download_image(self, image_url, filename):
        """Download and save image from URL or data URI"""
        try:
            # Create temp directory if it doesn't exist
            temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp')
            os.makedirs(temp_dir, exist_ok=True)
            
            file_path = os.path.join(temp_dir, filename)
            
            # Check if it's a data URI (base64 encoded image)
            if image_url.startswith('data:'):
                print(f"Processing base64 data URI for {filename}", flush=True)
                try:
                    # Extract the base64 data
                    header, data = image_url.split(',', 1)
                    image_data = base64.b64decode(data)
                    
                    # Try to open and verify it's a valid image
                    try:
                        img = Image.open(io.BytesIO(image_data))
                        # Convert to RGB if necessary (for JPEG)
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                        img.save(file_path, 'JPEG', quality=85)
                        print(f"[SUCCESS] Image saved from data URI: {filename}", flush=True)
                        return file_path
                    except Exception as img_error:
                        # If PIL fails, save as raw bytes
                        with open(file_path, 'wb') as f:
                            f.write(image_data)
                        print(f"[SUCCESS] Image saved (raw) from data URI: {filename}", flush=True)
                        return file_path
                        
                except Exception as data_error:
                    print(f"[ERROR] Failed to process data URI for {filename}: {data_error}", flush=True)
                    return None
            
            # Handle regular HTTP/HTTPS URLs
            elif image_url.startswith(('http://', 'https://')):
                print(f"Downloading from URL for {filename}")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                response = requests.get(image_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Try to open and verify it's a valid image
                try:
                    img = Image.open(io.BytesIO(response.content))
                    # Convert to RGB if necessary (for JPEG)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    img.save(file_path, 'JPEG', quality=85)
                    print(f"[SUCCESS] Image saved from URL: {filename}")
                    return file_path
                except Exception as img_error:
                    # If PIL fails, save as raw bytes
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[SUCCESS] Image saved (raw) from URL: {filename}")
                    return file_path
            
            else:
                print(f"[ERROR] Unsupported image URL format for {filename}: {image_url[:50]}...")
                return None
                
        except Exception as e:
            print(f"[ERROR] Failed to download image {filename}: {e}")
            return None
    
    def select_articles_with_images(self, articles, num_articles=3):
        """Select the best articles ensuring at least one has a featured image"""
        if not articles:
            return []
        
        # Separate articles with and without images
        articles_with_images = [article for article in articles if article.get('image_url')]
        articles_without_images = [article for article in articles if not article.get('image_url')]
        
        print(f"Found {len(articles_with_images)} articles with images out of {len(articles)} total articles")
        
        selected_articles = []
        
        # Adjust num_articles if we have fewer total articles available
        actual_num_articles = min(num_articles, len(articles))
        
        if len(articles_with_images) >= actual_num_articles:
            # If we have enough articles with images, just take the required number
            selected_articles = articles_with_images[:actual_num_articles]
            print(f"[SUCCESS] Selected {actual_num_articles} articles, all with featured images")
        elif len(articles_with_images) > 0:
            # We have some articles with images, but not enough
            # Take all articles with images first
            selected_articles.extend(articles_with_images)
            
            # Fill the remaining slots with articles without images (prioritize first ones)
            remaining_slots = actual_num_articles - len(articles_with_images)
            selected_articles.extend(articles_without_images[:remaining_slots])
            
            print(f"[SUCCESS] Selected {len(selected_articles)} articles: {len(articles_with_images)} with images, {len(selected_articles) - len(articles_with_images)} without images")
        else:
            # No articles have images, return None to indicate failure
            print(f"[WARNING] No articles found with featured images out of {len(articles)} articles searched")
            return None
        
        return selected_articles[:actual_num_articles]
    
    def check_keyword_exists(self, keyword):
        """Check if a keyword already exists in articles.json"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        articles_json_path = os.path.join(script_dir, "..", "json", "articles.json")
        
        try:
            with open(articles_json_path, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            
            # Check if any article has this keyword (case-insensitive)
            keyword_lower = keyword.lower()
            for article in articles:
                if article.get('keyword', '').lower() == keyword_lower:
                    return True
            
            return False
            
        except FileNotFoundError:
            print(f"Articles file not found: {articles_json_path}")
            return False
        except json.JSONDecodeError:
            print(f"Invalid JSON in articles file: {articles_json_path}")
            return False
        except Exception as e:
            print(f"Error reading articles file: {e}")
            return False

    def get_next_available_trend(self):
        """Get the next trend that doesn't already exist in articles.json"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "..", "json", "latest_trends.json")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            trends = data.get('trends', [])
            # Sort trends by rank to process them in order
            trends.sort(key=lambda x: x.get('rank', float('inf')))
            
            for trend in trends:
                trend_name = trend.get('trend_name')
                if trend_name:
                    if not self.check_keyword_exists(trend_name):
                        print(f"Found available trend: {trend_name} (Rank: {trend.get('rank')})")
                        return trend_name
                    else:
                        print(f"Skipping trend: {trend_name} (already exists in articles.json)")
            
            print("No new trends found - all trends already exist in articles.json")
            return None
            
        except FileNotFoundError:
            print(f"File not found: {json_path}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {json_path}")
            return None
        except Exception as e:
            print(f"Error reading trends file: {e}")
            return None

    def get_top_trend(self):
        """Get the trend with rank 1 from latest_trends.json (kept for backward compatibility)"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "..", "json", "latest_trends.json")
        
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            trends = data.get('trends', [])
            for trend in trends:
                if trend.get('rank') == 1:
                    return trend.get('trend_name')
            
            print("No trend with rank 1 found")
            return None
            
        except FileNotFoundError:
            print(f"File not found: {json_path}")
            return None
        except json.JSONDecodeError:
            print(f"Invalid JSON in file: {json_path}")
            return None
        except Exception as e:
            print(f"Error reading trends file: {e}")
            return None
    
    def search_articles_with_bing(self, query, num_articles=3, max_search=50):
        """Search for articles using Bing News with Selenium"""
        try:
            # Append "news india" to the query as requested
            search_query = f"{query} news india"
            encoded_query = quote(search_query)
            bing_url = f"https://www.bing.com/news/search?q={encoded_query}"
            
            print(f"Searching Bing News for: {search_query}")
            print(f"Keyword filter: '{query}' (case-insensitive)")
            print(f"URL: {bing_url}")
            
            # Setup driver if not already done
            if not self.driver:
                self.setup_driver()
            
            # Navigate to Bing News
            self.driver.get(bing_url)
            
            # Wait for any news results to load with multiple selector options
            selectors_to_try = [
                ".news-card",
                "[data-module='NewsArticle']", 
                ".newsitem",
                ".news-item",
                "article",
                ".contentArea .na_cnt",
                ".algocore"
            ]
            
            results_loaded = False
            for selector in selectors_to_try:
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    print(f"Found results using selector: {selector}")
                    results_loaded = True
                    break
                except:
                    continue
            
            if not results_loaded:
                print("No standard news results found, trying general content...")
                time.sleep(3)
            
            # Load more dynamic content by scrolling
            self._load_more_bing_results()
            
            # Extract articles using multiple selector strategies
            articles = []
            articles.extend(self._extract_bing_articles_method1(query, max_search))
            
            if len(articles) < num_articles:
                print(f"Method 1 found {len(articles)} articles, trying additional methods...")
                articles.extend(self._extract_bing_articles_method2(query, max_search - len(articles)))
            
            if len(articles) < num_articles:
                print(f"Method 2 found {len(articles)} total articles, trying fallback method...")
                articles.extend(self._extract_bing_articles_fallback(query, max_search - len(articles)))
            
            # Remove duplicates based on URL
            seen_urls = set()
            unique_articles = []
            for article in articles:
                if article['link'] and article['link'] not in seen_urls:
                    seen_urls.add(article['link'])
                    unique_articles.append(article)
            
            articles = unique_articles
            print(f"\nTotal unique matching articles found: {len(articles)}")
            
            # If we have fewer than required articles, still proceed with what we have
            if len(articles) < num_articles:
                print(f"Warning: Only found {len(articles)} matching articles (requested {num_articles})")
                if len(articles) == 0:
                    print("No articles found matching the keyword filter")
                    return []
            
            # Select best articles ensuring at least one has a featured image
            return self.select_articles_with_images(articles, num_articles)
            
        except Exception as e:
            print(f"Error searching with Bing: {e}")
            # Return fallback articles
            return [{
                'title': f"Latest News about {query}",
                'link': '',
                'source': 'Bing News Search',
                'time': 'Recent',
                'snippet': f"Recent developments about {query}",
                'image_url': ''
            }]
    
    
    def fetch_article_content(self, url, title="", source=""):
        """Analyze article URL and generate content using Google Gemini"""
        # If no URL is provided, use Gemini to generate detailed content
        if not url or url == "":
            return self.generate_article_content_with_gemini(title, source)
        
        try:
            print(f"Analyzing content using Gemini for: {title[:50]}...")
            
            # Use Gemini to analyze the URL and generate content
            content_prompt = f"""
            Based on the article title "{title}" and URL "{url}", please provide a detailed news article analysis with INDIAN context and perspective.
            
            Please analyze and provide:
            1. A comprehensive overview of the topic from an Indian perspective
            2. Key facts and details relevant to India
            3. Background information with Indian context
            4. Current developments and their impact on India
            5. Implications for Indian society, economy, or politics
            6. Market analysis or industry impact (if applicable)
            7. How this news affects Indian citizens or the Indian market
            8. Future outlook and predictions
            
            FOCUS ON:
            - Indian angle and relevance
            - Local impact and implications
            - Indian government or institutional response (if applicable)
            - Regional or state-specific details (if relevant)
            - Connection to Indian policies, culture, or economy
            - Technical specifications and features (if it's a product launch)
            - Competitive landscape in India (if applicable)
            
            Write this as a comprehensive analysis with proper paragraphs. Ensure the content is:
            - Factual and news-oriented
            - Relevant to Indian readers
            - Current and up-to-date
            - Well-structured with clear information flow
            - Detailed and informative
            
            Keep the content informative and well-structured, around 400-600 words.
            If the topic is international news, focus on its impact or relevance to India.
            """
            
            response = self.model.generate_content(content_prompt)
            return response.text[:5000]  # Limit content length for API
            
        except Exception as e:
            print(f"Error analyzing content with Gemini: {e}")
            print("Falling back to basic content generation...")
            return self.generate_article_content_with_gemini(title, source)
    
    def generate_article_content_with_gemini(self, title, source=""):
        """Generate detailed article content using Gemini when URL is not available"""
        try:
            print(f"Generating content for: {title[:50]}...")
            
            content_prompt = f"""
            Based on the article title "{title}" from Indian news source "{source}", please provide a detailed news article content with INDIAN context and perspective.
            
            Please include:
            1. A comprehensive overview of the topic from an Indian perspective
            2. Key facts and details relevant to India
            3. Background information with Indian context
            4. Current developments and their impact on India
            5. Implications for Indian society, economy, or politics
            6. Relevant quotes from Indian officials, experts, or stakeholders (if applicable)
            7. How this news affects Indian citizens or the Indian market
            
            FOCUS ON:
            - Indian angle and relevance
            - Local impact and implications
            - Indian government or institutional response (if applicable)
            - Regional or state-specific details (if relevant)
            - Connection to Indian policies, culture, or economy
            
            Write this as a complete news article with proper paragraphs. Ensure the content is:
            - Factual and news-oriented (not opinion)
            - Relevant to Indian readers
            - Current and up-to-date
            - Well-structured with clear information flow
            
            Keep the content informative and well-structured, around 300-500 words.
            If the topic is international news, focus on its impact or relevance to India.
            """
            
            response = self.model.generate_content(content_prompt)
            
            # Add 60 second delay after Gemini API call
            print("Waiting 60 seconds before next API call...")
            time.sleep(60)
            
            return response.text[:5000]  # Limit content length
            
        except Exception as e:
            print(f"Error generating content with Gemini: {e}")
            return f"Article about {title}. Content could not be generated due to technical issues."
    
    def analyze_with_gemini(self, title, content, source):
        """Analyze article content with Gemini Flash 2.0 and produce ready-to-publish content"""
        try:
            prompt = f"""
            Based on this news article, write a comprehensive, ready-to-publish analysis article. If the original article is in Hindi or any other Indian language, translate it to English first, then provide the analysis.

            Article Title: {title}
            Source: {source}
            Content: {content}

            Write a complete, engaging article that includes:
            - A compelling introduction that hooks the reader
            - Key facts and developments from the news
            - Background context and significance
            - Impact analysis and implications
            - Expert insights or market reactions (if applicable)
            - Future outlook or what to watch for
            - A strong conclusion

            IMPORTANT REQUIREMENTS:
            - Use simple, clear English that can be easily understood by average Indian users
            - Avoid complex vocabulary, technical jargon, and complicated sentence structures
            - Write in a conversational, easy-to-read style
            - Make it ready for immediate publication
            - Do NOT include meta-commentary like "Here's a comprehensive analysis" or "This article provides"
            - Do NOT start with markdown headers like "##" - start directly with the content
            - Start directly with the content
            - Keep it engaging and informative for general readers
            - Length: 400-600 words
            - Focus on Indian context and relevance where applicable

            Write the article now:
            """
            
            print("Analyzing article with Gemini Flash 2.5...")
            response = self.model.generate_content(prompt)
            
            # Add 60 second delay after Gemini API call
            print("Waiting 60 seconds before next API call...")
            time.sleep(60)
            
            return response.text
            
        except Exception as e:
            print(f"Error analyzing with Gemini: {e}")
            return f"Error analyzing article: {str(e)}"
    
    def save_article_analysis(self, trend_name, articles_data):
        """Save the analyzed articles to temp/article_analysis.json"""
        filename = "article_analysis.json"
        filepath = os.path.join(self.temp_dir, filename)
        
        data_to_save = {
            "trend_searched": trend_name.lower(),
            "total_articles": len(articles_data),
            "articles": articles_data
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            
            print(f"\nArticle analysis saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving analysis: {e}")
            return None
    
    def run(self):
        """Main execution method"""
        # Ensure all output is unbuffered
        sys.stdout.flush()
        print("Starting Bing News Article Search and Analysis...", flush=True)
        print("="*60, flush=True)
        
        try:
            # Step 1: Get next available trend (that doesn't exist in articles.json)
            trend_name = self.get_next_available_trend()
            if not trend_name:
                print("Could not find any new trends to process. All trends already exist in articles.json.")
                return
            
            print(f"Next available trend found: {trend_name}", flush=True)
            
            # Step 2: Search for articles using Bing News with Selenium
            print(f"\nSearching for articles about: {trend_name}", flush=True)
            print("Will search through articles to find at least 3 matching the keyword with at least 1 featured image...", flush=True)
            
            articles = self.search_articles_with_bing(trend_name, 3)
            
            # Check if we have None (no articles with images found)
            if articles is None:
                print("\n" + "="*60)
                print("PROGRAM TERMINATED: No articles with featured images found!")
                print("Searched through available articles but none matching the keyword had featured images.")
                print("Skipping article analysis and JSON creation.")
                print("="*60)
                return
            
            if not articles:
                print("No articles found. Exiting.")
                return
            
            print(f"\n[SUCCESS] Selected {len(articles)} articles for analysis", flush=True)
            
            # Step 3: Fetch and analyze each article
            articles_data = []
            
            for i, article in enumerate(articles, 1):
                print(f"\n--- Processing Article {i} ---", flush=True)
                print(f"Title: {article['title']}", flush=True)
                
                # Download featured image if available
                image_path = None
                if article.get('image_url'):
                    print(f"Downloading featured image for article {i}...", flush=True)
                    image_filename = f"article_{i}.jpg"
                    image_path = self.download_image(article['image_url'], image_filename)
                else:
                    print(f"No featured image found for article {i}", flush=True)
                
                # Fetch full content
                content = self.fetch_article_content(article['link'], article['title'], article['source'])
                
                if content:
                    # Analyze with Gemini
                    analysis = self.analyze_with_gemini(article['title'], content, article['source'])
                    
                    article_data = {
                        "article_number": i,
                        "title": article['title'],
                        "url": article['link'],
                        "gemini_analysis": analysis
                    }
                    
                    articles_data.append(article_data)
                    
                    print(f"[SUCCESS] Article {i} analyzed successfully", flush=True)
                else:
                    print(f"[ERROR] Could not fetch content for article {i}", flush=True)
                    
                    # Still save basic info even without content
                    article_data = {
                        "article_number": i,
                        "title": article['title'],
                        "url": article['link'],
                        "gemini_analysis": "Content not available for analysis"
                    }
                    
                    articles_data.append(article_data)
            
            # Step 4: Save results
            if articles_data:
                self.save_article_analysis(trend_name, articles_data)
                print(f"\n[SUCCESS] Analysis complete! Results saved to temp/article_analysis.json", flush=True)
                
                # Show analysis summary
                print(f"[SUCCESS] Articles analyzed: {len(articles_data)} out of 3 articles", flush=True)
            else:
                print("\n[ERROR] No articles were successfully analyzed.", flush=True)
            
            print("\n" + "="*60)
            print("Bing News Article Search and Analysis Complete!")
        
        except Exception as e:
            print(f"Error during execution: {e}")
        finally:
            # Always close the driver
            self.close_driver()

def main():
    """Main function"""
    try:
        searcher = ArticleSearcher()
        searcher.run()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()