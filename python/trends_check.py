#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Trends Scraper for India - Last 4 Hours
Scrapes trending topics from Google Trends India with search volumes and active status
"""

import time
import random
import re
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Fix Unicode output issues on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

class GoogleTrendsScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Setup Chrome driver with stealth options to avoid detection"""
        chrome_options = Options()
        
        # Headless mode
        chrome_options.add_argument("--headless")
        
        # Stealth options to avoid detection
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to appear as regular browser
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Additional stealth options
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins-discovery")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            # Use webdriver-manager to automatically download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
        except Exception as e:
            print(f"Error setting up Chrome driver: {e}")
            print("Make sure Chrome browser is installed")
            raise
    
    def random_delay(self, min_seconds=1, max_seconds=3):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def is_english_text(self, text):
        """Check if text is primarily in English"""
        if not text:
            return False
        
        # Remove numbers, punctuation, and spaces
        clean_text = re.sub(r'[0-9\s\W]', '', text)
        
        if not clean_text:
            return False
        
        # Count English characters (basic Latin alphabet)
        english_chars = sum(1 for char in clean_text if ord(char) < 128 and char.isalpha())
        total_chars = len(clean_text)
        
        # Consider text English if at least 70% of characters are English
        return (english_chars / total_chars) >= 0.7 if total_chars > 0 else False
    
    def scrape_trends(self):
        """Scrape Google Trends data for India in last 4 hours"""
        url = "https://trends.google.com/trending?geo=IN&hours=4"
        
        try:
            print("Loading Google Trends page...")
            self.driver.get(url)
            
            # Wait for page to load and add random delay
            self.random_delay(3, 5)
            
            # Wait for the table to be present
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.presence_of_element_located((By.XPATH, "//table/tbody[2]")))
            
            print("Page loaded successfully. Extracting trends data...")
            
            trends_data = []
            
            # Extract data for all 25 rows
            for i in range(1, 26):
                try:
                    # XPath for trend name
                    trend_xpath = f"/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[{i}]/td[2]/div[1]"
                    
                    # XPath for search volume
                    volume_xpath = f"/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[{i}]/td[3]/div/div[1]"
                    
                    # XPath for active status
                    status_xpath = f"/html/body/c-wiz/div/div[5]/div[1]/c-wiz/div/div[2]/div[1]/div[1]/div[1]/table/tbody[2]/tr[{i}]/td[4]/div[2]/div/div"
                    
                    # Extract trend name
                    try:
                        trend_element = self.driver.find_element(By.XPATH, trend_xpath)
                        trend_name = trend_element.text.strip()
                    except NoSuchElementException:
                        trend_name = "N/A"
                    
                    # Extract search volume
                    try:
                        volume_element = self.driver.find_element(By.XPATH, volume_xpath)
                        search_volume = volume_element.text.strip()
                    except NoSuchElementException:
                        search_volume = "N/A"
                    
                    # Extract active status
                    try:
                        status_element = self.driver.find_element(By.XPATH, status_xpath)
                        active_status = status_element.text.strip()
                        if not active_status:
                            # Try to get class or other attributes that might indicate status
                            active_status = status_element.get_attribute("class") or "Unknown"
                    except NoSuchElementException:
                        active_status = "N/A"
                    
                    # Only add if we have at least the trend name
                    if trend_name and trend_name != "N/A":
                        trend_data = {
                            "rank": i,
                            "trend_name": trend_name,
                            "search_volume": search_volume,
                            "active_status": active_status
                        }
                        trends_data.append(trend_data)
                        print(f"Extracted trend {i}: {trend_name}")
                    
                    # Small delay between extractions
                    self.random_delay(0.1, 0.3)
                    
                except Exception as e:
                    print(f"Error extracting data for row {i}: {e}")
                    continue
            
            # Filter for English trends with Active status
            filtered_trends = self.filter_trends(trends_data)
            return filtered_trends
            
        except TimeoutException:
            print("Timeout waiting for page to load. The page structure might have changed.")
            return []
        except Exception as e:
            print(f"Error scraping trends: {e}")
            return []
    
    def parse_search_volume(self, volume_str):
        """Parse search volume string to numeric value"""
        if not volume_str or volume_str == "N/A":
            return 0
        
        # Remove any extra whitespace
        volume_str = volume_str.strip().upper()
        
        # Handle different formats
        if 'K+' in volume_str:
            # Convert 2K+ to 2000+
            number = volume_str.replace('K+', '').replace(',', '')
            try:
                return int(float(number) * 1000)
            except ValueError:
                return 0
        elif 'M+' in volume_str:
            # Convert 1M+ to 1000000+
            number = volume_str.replace('M+', '').replace(',', '')
            try:
                return int(float(number) * 1000000)
            except ValueError:
                return 0
        elif '+' in volume_str:
            # Handle cases like 500+
            number = volume_str.replace('+', '').replace(',', '')
            try:
                return int(number)
            except ValueError:
                return 0
        else:
            # Try to parse as regular number
            try:
                return int(volume_str.replace(',', ''))
            except ValueError:
                return 0
    
    def filter_trends(self, trends_data):
        """Filter trends to show only English trends with Active status"""
        filtered_trends = []
        
        print("\nFiltering trends for English language and Active status...")
        
        for trend in trends_data:
            trend_name = trend.get('trend_name', '')
            active_status = trend.get('active_status', '').lower()
            
            # Check if trend is in English
            is_english = self.is_english_text(trend_name)
            
            # Check if status contains "active" (case insensitive)
            is_active = 'active' in active_status or active_status == 'active'
            
            if is_english and is_active:
                # Parse search volume to numeric value
                original_volume = trend.get('search_volume', '')
                numeric_volume = self.parse_search_volume(original_volume)
                
                # Add parsed volume to trend data
                trend['search_volume_numeric'] = numeric_volume
                trend['search_volume_display'] = original_volume.replace('K+', '000+').replace('M+', '000000+') if original_volume != "N/A" else "N/A"
                
                filtered_trends.append(trend)
                print(f"[+] Included: {trend_name} (Volume: {original_volume} -> {numeric_volume}, Status: {trend['active_status']})")
            else:
                reason = []
                if not is_english:
                    reason.append("not English")
                if not is_active:
                    reason.append("not Active")
                print(f"[-] Excluded: {trend_name} ({', '.join(reason)})")
        
        # Sort by search volume in descending order, maintaining original rank as secondary sort
        filtered_trends.sort(key=lambda x: (-x['search_volume_numeric'], x['rank']))
        
        # Reassign ranks after sorting (1, 2, 3, etc.)
        for index, trend in enumerate(filtered_trends, 1):
            trend['rank'] = index
        
        print(f"\nFiltered and sorted {len(filtered_trends)} trends from {len(trends_data)} total trends")
        return filtered_trends
    
    def display_results(self, trends_data):
        """Display the scraped trends data in a formatted way"""
        if not trends_data:
            print("No trends data found.")
            return
        
        print("\n" + "="*80)
        print("GOOGLE TRENDS - INDIA (Last 4 Hours)")
        print("FILTERED RESULTS: English Language + Active Status Only")
        print("SORTED BY: Search Volume (Descending)")
        print(f"Scraped on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        print(f"{'Rank':<5} {'Trend Name':<40} {'Search Volume':<15} {'Status':<15}")
        print("-"*80)
        
        for trend in trends_data:
            print(f"{trend['rank']:<5} {trend['trend_name']:<40} {trend['search_volume_display']:<15} {trend['active_status']:<15}")
        
        print("-"*80)
        print(f"Total trends found: {len(trends_data)}")
    
    def save_to_json(self, trends_data, filename="latest_trends.json"):
        """Save trends data to JSON file in json folder"""
        if not trends_data:
            return
        
        # Prepare data for JSON (remove internal numeric field, keep display format)
        json_trends = []
        for trend in trends_data:
            json_trend = {
                "rank": trend["rank"],
                "trend_name": trend["trend_name"],
                "search_volume": trend["search_volume_display"],
                "active_status": trend["active_status"]
            }
            json_trends.append(json_trend)
        
        data_to_save = {
            "timestamp": datetime.now().isoformat(),
            "location": "India",
            "timeframe": "Last 4 hours",
            "filter_criteria": "English language + Active status only",
            "sort_order": "Descending by search volume",
            "total_filtered_trends": len(trends_data),
            "trends": json_trends
        }
        
        # Save to temp folder using absolute path
        temp_folder_path = os.path.join(PROJECT_ROOT, "temp")
        full_path = os.path.join(temp_folder_path, filename)
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=2, ensure_ascii=False)
            print(f"\nData saved to {full_path}")
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()

def main():
    """Main function to run the Google Trends scraper"""
    scraper = None
    
    try:
        print("Starting Google Trends Scraper for India...")
        scraper = GoogleTrendsScraper()
        
        # Scrape trends data
        trends_data = scraper.scrape_trends()
        
        # Display results
        scraper.display_results(trends_data)
        
        # Save to JSON file
        scraper.save_to_json(trends_data)
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if scraper:
            scraper.close()
        print("\nScraping completed.")

if __name__ == "__main__":
    main()