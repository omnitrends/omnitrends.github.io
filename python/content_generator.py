import json
import os
import re
import sys
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def fetch_trend_name():
    """
    Fetch the keyword key's value from temp/keyword_selection.json
    
    Returns:
        str: The keyword value from the JSON file
    """
    keyword_selection_path = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
    try:
        with open(keyword_selection_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data.get('keyword', '')
    except FileNotFoundError:
        print(f"Error: {keyword_selection_path} file not found")
        return ""
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in keyword_selection.json")
        return ""

def generate_article_title(keyword):
    """
    Generate an SEO-friendly article title using Gemini API with Google Search capabilities
    
    Args:
        keyword (str): The main keyword for the article
        
    Returns:
        str: Generated SEO-friendly title containing the keyword
    """
    # Get Gemini API key from environment
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return ""
    
    # Configure the client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Define the grounding tool for real-time search
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    # Configure generation settings
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )
    
    # Create a powerful prompt for title generation
    prompt = f"""
    Search for the latest news about "{keyword}" in Indian context and generate ONE compelling, SEO-friendly article title.
    
    Requirements:
    - Generate ONLY ONE title, not multiple options
    - Title must contain the exact keyword: "{keyword}"
    - STRICT LIMIT: Maximum 60 characters only
    - Focus on why this keyword is trending in Indian news today
    - Make it clickable and engaging for Indian audience
    - Use action words and emotional triggers
    - Make it Google Discover and AdSense friendly
    - Avoid clickbait but make it compelling
    - Respond with ONLY the final title, no explanations, no bullet points, no options
    
    Generate the single best title (maximum 60 characters):
    """
    
    try:
        # Make the request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        return response.text.strip()
    except Exception as e:
        print(f"Error generating title: {e}")
        sys.exit(1)

def categorize_article(keyword, title):
    """
    Categorize the generated article using Gemini API
    
    Args:
        keyword (str): The main keyword for the article
        title (str): The generated title
        
    Returns:
        str: Selected category from the predefined list
    """
    # Get Gemini API key from environment
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return "News"  # Default fallback
    
    # Configure the client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Create a prompt for categorization
    prompt = f"""
    Based on the keyword "{keyword}" and title "{title}", categorize this article under EXACTLY ONE of these categories:

    Technology
    Lifestyle
    Business
    Innovation
    News
    Health
    Entertainment
    Finance
    Science
    Travel
    Food
    Sports

    Requirements:
    - You MUST select only ONE category from the list above
    - Choose the most appropriate category based on the content theme
    - Respond with ONLY the category name, no explanations
    - If unsure, default to "News"

    Category:
    """
    
    try:
        # Make the request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        category = response.text.strip()
        
        # Validate the category is in our allowed list
        allowed_categories = [
            "Technology", "Lifestyle", "Business", "Innovation", 
            "News", "Health", "Entertainment", "Finance", 
            "Science", "Travel", "Food", "Sports"
        ]
        
        if category in allowed_categories:
            return category
        else:
            return "News"  # Default fallback
            
    except Exception as e:
        print(f"Error categorizing article: {e}")
        return "News"  # Default fallback

def get_current_date():
    """
    Get current system date in the required format
    
    Returns:
        str: Current date in format "01 August 2025"
    """
    try:
        current_date = datetime.now()
        return current_date.strftime("%d %B %Y")
    except Exception as e:
        print(f"Error getting current date: {e}")
        return datetime.now().strftime("%d %B %Y")

def generate_article_excerpt(keyword, title):
    """
    Generate an SEO-friendly article excerpt using Gemini API with Google Search capabilities
    
    Args:
        keyword (str): The main keyword for the article
        title (str): The generated title for context
        
    Returns:
        str: Generated SEO-friendly excerpt containing the keyword
    """
    # Get Gemini API key from environment
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return ""
    
    # Configure the client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Define the grounding tool for real-time search
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    # Configure generation settings
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )
    
    # Create a powerful prompt for excerpt generation
    prompt = f"""
    Search for the latest news about "{keyword}" in Indian context and generate a compelling article excerpt.
    
    Article Title: "{title}"
    Main Keyword: "{keyword}"
    
    Requirements:
    - Excerpt must contain the exact keyword: "{keyword}"
    - Do not repeat the title in the excerpt
    - Do not use inverted commas in the excerpt
    - Change the case of keyword if required
    - STRICT LIMIT: Maximum 150 characters only
    - Focus on why this keyword is trending in Indian news
    - Write for Indian audience in simple, clear English
    - Make it engaging and informative
    - Include a call-to-action or curiosity element
    - Make it Google Discover and AdSense friendly
    - Summarize the key point that makes this newsworthy in India in maximum 150 characters only
    - Avoid clickbait but make it compelling
    - Respond with ONLY the final excerpt, no explanations, no bullet points, no options
    
    Based on current Indian news context, generate only the excerpt (maximum 150 characters, no explanations):
    """
    
    try:
        # Make the request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        return response.text.strip()
    except Exception as e:
        print(f"Error generating excerpt: {e}")
        sys.exit(1)

def generate_article_content(keyword, title, excerpt):
    """
    Generate a complete SEO-optimized article using Gemini API with Google Search capabilities
    
    Args:
        keyword (str): The main keyword for the article
        title (str): The generated title
        excerpt (str): The generated excerpt
        
    Returns:
        str: Generated production-ready article content with proper HTML formatting
    """
    # Get Gemini API key from environment
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return ""
    
    # Configure the client
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Define the grounding tool for real-time search
    grounding_tool = types.Tool(
        google_search=types.GoogleSearch()
    )
    
    # Configure generation settings
    config = types.GenerateContentConfig(
        tools=[grounding_tool]
    )
    
    # Create a comprehensive prompt for article generation
    prompt = f"""
    Search for the latest news about "{keyword}" in Indian context and write a comprehensive article.
    
    Context Information (DO NOT INCLUDE IN ARTICLE):
    - Article Title: "{title}"
    - Article Excerpt: "{excerpt}"
    - Main Keyword: "{keyword}"
    
    Requirements:
    - STRICT LIMIT: Write MAXIMUM 300 words (count every word, strictly enforce this limit)
    - Use simple, plain English suitable for Indian audience
    - KEYWORD DENSITY: Include the keyword "{keyword}" exactly 9 times throughout the article (3% density for 300 words)
    - Do not use inverted commas in the article
    - Change the case of keyword if required
    - Focus on why this keyword is trending in Indian news today
    - Write for Indian audience in simple, clear English
    - Focus on Indian news context and why this matters to Indians
    - Use Markdown heading syntax: ## for subheadings, ### for sub-subheadings
    - Make it production-ready with no meta text or placeholders
    - DO NOT include the title, excerpt, or any metadata in the article content
    - Create well-structured, SEO-optimized content with natural subheadings
    - Choose your own relevant subheadings based on the content (don't use generic ones)
    - Include relevant facts, figures, and current developments
    - Write in an informative, engaging tone
    - MUST be well-structured with clear paragraphs and logical flow
    - MUST end with a proper conclusion section
    
    Article Structure Guidelines:
    - Opening paragraph (introduce the topic and its relevance)
    - Choose 2-3 relevant subheadings (##) based on the content
    - Use sub-subheadings (###) if needed for better organization
    - Include a conclusion section with appropriate heading
    - Ensure natural keyword placement throughout
    
    Write ONLY the article content (no title, no excerpt, no metadata). Start directly with the opening paragraph. Use Markdown syntax for headings. Maximum 300 words with exactly 9 mentions of "{keyword}".
    """
    
    try:
        # Make the request
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        return response.text.strip()
    except Exception as e:
        print(f"Error generating article: {e}")
        sys.exit(1)

def save_article_to_file(keyword, title, excerpt, content):
    """
    Save the generated article to temp/final.md with production-ready formatting
    
    Args:
        keyword (str): The main keyword
        title (str): The generated title
        excerpt (str): The generated excerpt
        content (str): The generated article content
    """
    try:
        # Create production-ready content without H1 title (HTML template handles it)
        formatted_content = f"""{content}
"""
        
        # Ensure the temp directory exists
        temp_dir = os.path.join(PROJECT_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Write to temp/final.md
        final_md_path = os.path.join(PROJECT_ROOT, 'temp', 'final.md')
        with open(final_md_path, 'w', encoding='utf-8') as file:
            file.write(formatted_content)
        
        print("Article successfully saved to temp/final.md")
        time.sleep(30)
        
    except Exception as e:
        print(f"Error saving article to file: {e}")

def update_keyword_selection_json(keyword, title, category, date, excerpt):
    """
    Update temp/keyword_selection.json with the new article information
    
    Args:
        keyword (str): The original keyword
        title (str): The generated title
        category (str): The selected category
        date (str): The current date
        excerpt (str): The generated excerpt
    """
    try:
        # Generate ID from title (separated by -)
        # Remove special characters and replace spaces with hyphens
        article_id = re.sub(r'[^\w\s-]', '', title.lower())
        article_id = re.sub(r'[-\s]+', '-', article_id).strip('-')
        
        # Create the new data structure
        new_data = {
            "id": article_id,
            "keyword": keyword,
            "title": title,
            "category": category,
            "date": date,
            "url": f"articles/{article_id}.html",
            "excerpt": excerpt
        }
        
        # Ensure the temp directory exists
        temp_dir = os.path.join(PROJECT_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Write the updated JSON
        keyword_selection_path = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
        with open(keyword_selection_path, 'w', encoding='utf-8') as file:
            json.dump(new_data, file, indent=2, ensure_ascii=False)
        
        print("Successfully updated temp/keyword_selection.json")
        
    except Exception as e:
        print(f"Error updating keyword_selection.json: {e}")

def main():
    """
    Main function to orchestrate the content generation process
    """
    # Fetch the trend name
    keyword = fetch_trend_name()
    
    if not keyword:
        print("No keyword found. Exiting.")
        return
    
    print(f"Generating content for keyword: {keyword}")
    
    # Generate title
    print("Generating article title...")
    title = generate_article_title(keyword)
    print(f"Generated Title: {title}")
    
    # Wait 30 seconds before next API call
    print("Waiting 30 seconds before next API call...")
    time.sleep(30)
    
    # Categorize article
    print("Categorizing article...")
    category = categorize_article(keyword, title)
    print(f"Selected Category: {category}")
    
    # Get current date
    print("Fetching current date...")
    current_date = get_current_date()
    print(f"Current Date: {current_date}")
    
    # Wait 30 seconds before next API call
    print("Waiting 30 seconds before next API call...")
    time.sleep(30)
    
    # Generate excerpt
    print("Generating article excerpt...")
    excerpt = generate_article_excerpt(keyword, title)
    print(f"Generated Excerpt: {excerpt}")
    
    # Wait 30 seconds before next API call
    print("Waiting 30 seconds before next API call...")
    time.sleep(30)
    
    # Generate article content
    print("Generating article content...")
    article_content = generate_article_content(keyword, title, excerpt)
    print("Generated Article Content:")
    print(article_content)
    
    # Save article to file
    print("Saving article to temp/final.md...")
    save_article_to_file(keyword, title, excerpt, article_content)
    
    # Update keyword_selection.json with new structure
    print("Updating temp/keyword_selection.json...")
    update_keyword_selection_json(keyword, title, category, current_date, excerpt)
    
    return {
        'keyword': keyword,
        'title': title,
        'category': category,
        'date': current_date,
        'excerpt': excerpt,
        'content': article_content
    }

if __name__ == "__main__":
    main()