# -*- coding: utf-8 -*-
import json
import glob
import random
import os
import sys
import time
import re
from datetime import datetime
from dotenv import load_dotenv

# Try to import Google Generative AI with better error handling
try:
    import google.generativeai as genai
    print("Google Generative AI imported successfully", flush=True)
except ImportError as e:
    print(f"Error importing Google Generative AI: {e}", flush=True)
    print("Please ensure google-generativeai is installed: pip install google-generativeai", flush=True)
    sys.exit(1)

from PIL import Image
from io import BytesIO
import PIL.Image

# Fix Unicode output issues on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Load environment variables
load_dotenv()

def load_articles():
    """Load articles from article_analysis.json"""
    # Get the script directory and construct path to temp directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level from python/ to project root
    temp_file_path = os.path.join(project_root, 'temp', 'article_analysis.json')
    
    print(f"Looking for article_analysis.json at: {temp_file_path}", flush=True)
    
    if not os.path.exists(temp_file_path):
        print(f"ERROR: File not found at {temp_file_path}", flush=True)
        print(f"Current working directory: {os.getcwd()}", flush=True)
        print(f"Script directory: {script_dir}", flush=True)
        print(f"Project root: {project_root}", flush=True)
        
        # List contents of temp directory for debugging
        temp_dir = os.path.join(project_root, 'temp')
        if os.path.exists(temp_dir):
            print(f"Contents of temp directory ({temp_dir}):", flush=True)
            for item in os.listdir(temp_dir):
                print(f"  - {item}", flush=True)
        else:
            print(f"Temp directory does not exist: {temp_dir}", flush=True)
        
        raise FileNotFoundError(f"article_analysis.json not found at {temp_file_path}")
    
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def generate_clickbait_title(articles_data):
    """Generate an eye-catching title using dark psychology tricks"""
    # Configure Gemini API
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Get the trend topic
    trend_topic = articles_data.get('trend_searched', 'trending topic')
    
    prompt = f"""Create a compelling, SEO-optimized title for an article about "{trend_topic}" that attracts Indian readers while maintaining credibility and avoiding repetitive patterns.

CRITICAL REQUIREMENT: The title MUST contain the exact keyword "{trend_topic}" somewhere in it.

TITLE VARIETY REQUIREMENTS:
- Avoid overused words like "Shocking", "Secret", "Urgent" in every title
- Vary the psychological approach for each article
- Use different title structures and formats
- Balance curiosity with credibility

Choose ONE of these Google Discover-friendly approaches (rotate for variety):
1. EDUCATIONAL: "Understanding {trend_topic}: A Guide for Indians"
2. INFORMATIVE: "What Indians Should Know About {trend_topic}"
3. ANALYTICAL: "How {trend_topic} Affects Indian Families Today"
4. EXPLANATORY: "The {trend_topic} Situation: Facts for Indians"
5. HELPFUL: "{trend_topic} Explained: What It Means for India"
6. CONTEXTUAL: "{trend_topic} and Its Impact on Indian Society"
7. FACTUAL: "Breaking Down {trend_topic}: Indian Perspective"
8. PRACTICAL: "{trend_topic}: Essential Information for Indians"

The title should be:
- Maximum 60 characters for SEO
- Target Indian audience specifically
- Use simple, conversational English
- Avoid repetitive power words (shocking, secret, urgent, revealed)
- Sound informative and trustworthy (Google Discover friendly)
- MUST include the exact keyword "{trend_topic}" in the title
- Do NOT use single asterisks (*) around words for emphasis
- Create genuine interest without false urgency
- Be factual and educational in tone
- Avoid clickbait language that could hurt AdSense approval
- Sound like a helpful news article or educational piece

GOOGLE DISCOVER COMPLIANCE:
- Avoid sensational language
- Use authoritative, informative tone
- Make titles that deliver on their promise
- Focus on providing value to readers
- Ensure family-friendly content approach

Generate only the title, nothing else. Remember: The title MUST contain "{trend_topic}" and should be Google Discover and AdSense compliant."""

    response = model.generate_content(prompt)
    
    print("Waiting 60 seconds before next API call...", flush=True)
    time.sleep(60)
    
    # Post-process the title to remove single asterisks
    title = response.text.strip()
    
    # Remove words wrapped in single asterisks (e.g., *word* becomes word)
    title = re.sub(r'\*([^*]+)\*', r'\1', title)
    
    return title.title()

def update_json_with_title(title):
    """Update article_analysis.json with generated title"""
    # Get the script directory and construct path to temp directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level from python/ to project root
    temp_file_path = os.path.join(project_root, 'temp', 'article_analysis.json')
    
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create ordered dictionary to maintain field order
    ordered_data = {}
    ordered_data['trend_searched'] = data.get('trend_searched')
    ordered_data['total_articles'] = data.get('total_articles')
    ordered_data['articles'] = data.get('articles')
    
    # Add gemini_title after articles array
    ordered_data['gemini_title'] = title
    
    # Preserve any existing metadata fields
    if 'excerpt' in data:
        ordered_data['excerpt'] = data['excerpt']
    if 'date' in data:
        ordered_data['date'] = data['date']
    if 'category' in data:
        ordered_data['category'] = data['category']
    
    # Save updated JSON with proper ordering
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        json.dump(ordered_data, f, indent=2, ensure_ascii=False)
    
    return title

def generate_article_content(articles_data, title):
    """Generate an SEO-optimized article from all article analyses using Gemini"""
    # Configure Gemini API
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Combine all article analyses
    combined_text = ""
    for article in articles_data['articles']:
        combined_text += f"\n\n{article['gemini_analysis']}"
    
    trend_topic = articles_data.get('trend_searched', 'trending topic')
    
    prompt = f"""You are an expert SEO copywriter who writes Google Discover and AdSense-approved articles for Indian readers about "{trend_topic}". Use the title "{title}" as H1.

CRITICAL REQUIREMENTS:
1. Write in simple, conversational English that Indians understand easily
2. Target Indian audience specifically with local context and references
3. Make it sound completely human-written, not AI-generated
4. STRICTLY 300-350 words maximum (Google Discover optimization)
5. Structure for Google Discover and AdSense approval
6. Use proper markdown formatting with headers (H1, H2, H3)
7. CRITICAL: Do NOT use single asterisks (*) before, after or around words for emphasis. Use regular text only.

GOOGLE DISCOVER & ADSENSE COMPLIANCE:
- Avoid sensational or misleading claims
- Provide factual, helpful information
- Use authoritative tone without clickbait language
- Include educational value in every paragraph
- Avoid controversial or sensitive topics inappropriately
- Ensure content matches title promise exactly
- Use family-friendly language throughout

STRUCTURE VARIETY (Choose ONE format to avoid repetition):

FORMAT A - Informative:
# {title}
## Introduction (Why this matters to Indians - 2-3 sentences)
## Key Information (Main facts and details)
## What This Means for Indians (Practical implications)
## Conclusion (Actionable takeaway or thoughtful question)

FORMAT B - Explanatory:
# {title}
## Background Context (Setting up the topic for Indian readers)
## Current Situation (What's happening now)
## Impact Analysis (How it affects Indian families/individuals)
## Moving Forward (What to expect or do next)

FORMAT C - Educational:
# {title}
## Understanding the Basics (Simple explanation for everyone)
## Key Points to Remember (Important facts and figures)
## Practical Applications (How this applies to daily life)
## Final Thoughts (Summary with engaging question)

SEO & ENGAGEMENT REQUIREMENTS:
- Use the main keyword "{trend_topic}" naturally 3-4 times
- Include related keywords naturally
- Write engaging but factual content
- Use short paragraphs (2-3 sentences max)
- Include 1-2 engaging questions for readers
- Add specific Indian examples and context
- Maintain reader interest without sensationalism

TONE GUIDELINES:
- Match the tone to the title's promise (avoid tonal inconsistency)
- Be informative and helpful, not just attention-grabbing
- Provide genuine value and insights
- Use relatable examples from Indian context
- Avoid false urgency or manufactured drama
- Make it educational and trustworthy
- Sound like a knowledgeable friend explaining something important

Based on these articles:
{combined_text}

Generate ONLY the markdown article content, no explanations or meta-text. Choose the most appropriate format (A, B, or C) based on the topic. Ensure content is valuable, factual, and AdSense-friendly."""

    response = model.generate_content(prompt)
    
    print("Waiting 60 seconds before next API call...", flush=True)
    time.sleep(60)
    
    # Post-process the content to remove single asterisks
    content = response.text
    
    # Remove words wrapped in single asterisks (e.g., *word* becomes word)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    
    return content

def get_random_image():
    """Get the image with largest dimensions from temp folder"""
    # Get the script directory and construct path to temp directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)  # Go up one level from python/ to project root
    temp_dir = os.path.join(project_root, 'temp')
    
    image_patterns = [
        os.path.join(temp_dir, '*.png'),
        os.path.join(temp_dir, '*.jpg'), 
        os.path.join(temp_dir, '*.jpeg')
    ]
    all_images = []
    
    for pattern in image_patterns:
        all_images.extend(glob.glob(pattern))
    
    if not all_images:
        print(f"No images found in temp folder: {temp_dir}", flush=True)
        if os.path.exists(temp_dir):
            print(f"Contents of temp directory:", flush=True)
            for item in os.listdir(temp_dir):
                print(f"  - {item}", flush=True)
        raise FileNotFoundError("No images found in temp folder")
    
    # Calculate dimensions for each image
    image_dimensions = []
    for image_path in all_images:
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                dimension_product = width * height
                image_dimensions.append((image_path, dimension_product))
        except Exception as e:
            print(f"Warning: Could not process image {image_path}: {e}", flush=True)
            continue
    
    if not image_dimensions:
        raise FileNotFoundError("No valid images found in temp folder")
    
    # Find the maximum dimension product
    max_dimension = max(image_dimensions, key=lambda x: x[1])[1]
    
    # Get all images with the maximum dimension product
    max_dimension_images = [img_path for img_path, dim in image_dimensions if dim == max_dimension]
    
    # If multiple images have the same max dimensions, choose randomly
    return random.choice(max_dimension_images)

def generate_new_image(source_image_path):
    """Generate a new image using Gemini vision model with image-to-image generation"""
    try:
        # Configure Gemini API
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        # Import the new Google GenAI client
        from google import genai
        from google.genai import types
        from PIL import Image
        from io import BytesIO
        
        # Load the source image
        source_image = PIL.Image.open(source_image_path)
        print(f"Loaded source image: {source_image_path}", flush=True)
        
        # Create the GenAI client
        client = genai.Client(api_key=gemini_api_key)
        
        # Create a prompt for image generation that's relevant to news/trending topics
        text_input = ('Generate an image based on this source image. '
                     'Create a modern, professional news article featured image '
                     'that would be suitable for trending topics and news content. '
                     'Make it visually appealing and engaging for Indian readers. '
                     'IMPORTANT: If the image contains human figures, ensure that all hands, feet, and fingers '
                     'are anatomically correct and properly formed. Avoid any disfigured, distorted, or '
                     'unnaturally shaped human body parts, especially hands, feet, and fingers. '
                     'Please generate an image.')
        
        print("Generating new image using Gemini vision model...", flush=True)
        
        # Generate content with both text and image input
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=[text_input, source_image],
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        print("Waiting 60 seconds before next API call...", flush=True)
        time.sleep(60)
        
        # Process the response
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(f"Generated image description: {part.text}", flush=True)
            elif part.inline_data is not None:
                # Convert the generated image data to PIL Image
                generated_image = Image.open(BytesIO(part.inline_data.data))
                print("Successfully generated new image using Gemini vision model", flush=True)
                return generated_image
        
        # If no image was generated, return None to indicate failure
        print("No image was generated in response, image generation failed", flush=True)
        return None
        
    except ImportError as e:
        print(f"Import error for Google GenAI: {e}", flush=True)
        print("Image generation not available, returning None", flush=True)
        return None
    except Exception as e:
        print(f"Error generating image with Gemini: {e}", flush=True)
        print("Image generation failed, returning None", flush=True)
        return None

def resize_image(image, target_size=(1200, 630)):
    """Resize image to target dimensions"""
    return image.resize(target_size, Image.Resampling.LANCZOS)

def generate_excerpt():
    """Generate a short excerpt from final.md content"""
    try:
        with open('temp/final.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Configure Gemini API
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = f"""Create a compelling 2-3 sentence excerpt from this article that would make Indian readers want to click and read more. 
        
        The excerpt should:
        - Be 150-200 characters maximum
        - Capture the main hook/interesting point
        - Be engaging and clickable
        - Sound natural and conversational for Indian audience
        - Do NOT use single asterisks (*) around words for emphasis
        
        Article content:
        {content}
        
        Generate only the excerpt text, nothing else."""
        
        response = model.generate_content(prompt)
        
        print("Waiting 60 seconds before next API call...", flush=True)
        time.sleep(60)
        
        # Post-process the excerpt to remove single asterisks
        excerpt = response.text.strip()
        
        # Remove words wrapped in single asterisks (e.g., *word* becomes word)
        excerpt = re.sub(r'\*([^*]+)\*', r'\1', excerpt)
        
        return excerpt
        
    except Exception as e:
        # Fallback excerpt if generation fails
        return "Discover the shocking truth behind this trending topic that every Indian should know about!"

def get_todays_date():
    """Get today's date in format '01 June 2025'"""
    today = datetime.now()
    return today.strftime("%d %B %Y")

def categorize_article():
    """Categorize the article using Gemini into one of the 12 predefined categories"""
    try:
        with open('temp/final.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Configure Gemini API
        gemini_api_key = os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        categories = ["Technology", "Lifestyle", "Business", "Innovation", "News", 
                     "Health", "Entertainment", "Finance", "Science", "Travel", "Food", "Sports"]
        
        prompt = f"""You must categorize this article into ONE of these 12 categories. Choose the MOST appropriate category:

        Categories: {', '.join(categories)}

        Article content:
        {content}

        CRITICAL REQUIREMENT: You MUST respond with ONLY ONE category name from the list above. No explanations, no additional text, just the single category name.

        Category:"""
        
        response = model.generate_content(prompt)
        
        print("Waiting 60 seconds before next API call...", flush=True)
        time.sleep(60)
        
        category = response.text.strip()
        
        # Validate that the response is one of the allowed categories
        if category in categories:
            return category
        else:
            # Fallback to most likely category based on content analysis
            content_lower = content.lower()
            if any(word in content_lower for word in ['football', 'sport', 'match', 'barcelona', 'kobe']):
                return "Sports"
            elif any(word in content_lower for word in ['tech', 'digital', 'streaming', 'app']):
                return "Technology"
            elif any(word in content_lower for word in ['business', 'market', 'economic']):
                return "Business"
            else:
                return "News"  # Default fallback
                
    except Exception as e:
        print(f"Error in categorization: {str(e)}", flush=True)
        return "News"  # Default fallback category

def update_json_with_metadata(excerpt, date, category):
    """Update article_analysis.json with excerpt, date, and category"""
    try:
        # Get the script directory and construct path to temp directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)  # Go up one level from python/ to project root
        temp_file_path = os.path.join(project_root, 'temp', 'article_analysis.json')
        
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Create ordered dictionary to maintain field order
        ordered_data = {}
        ordered_data['trend_searched'] = data.get('trend_searched')
        ordered_data['total_articles'] = data.get('total_articles')
        ordered_data['articles'] = data.get('articles')
        
        # Add gemini_title just above excerpt (if it exists)
        if 'gemini_title' in data:
            ordered_data['gemini_title'] = data['gemini_title']
        
        # Add new metadata fields
        ordered_data['excerpt'] = excerpt
        ordered_data['date'] = date
        ordered_data['category'] = category
        
        # Extract keyword from trend_searched (remove "(news india)" if present)
        trend_searched = data.get('trend_searched', '')
        keyword = trend_searched.replace('(news india)', '').strip()
        ordered_data['keyword'] = keyword
        
        # Save updated JSON with proper ordering
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            json.dump(ordered_data, f, indent=2, ensure_ascii=False)
        
        print(f"Updated JSON with:", flush=True)
        print(f"  Excerpt: {excerpt}", flush=True)
        print(f"  Date: {date}", flush=True)
        print(f"  Category: {category}", flush=True)
        print(f"  Keyword: {keyword}", flush=True)
        
    except Exception as e:
        print(f"Error updating JSON with metadata: {str(e)}", flush=True)

def main():
    try:
        # Load articles data
        print("Loading articles...", flush=True)
        articles_data = load_articles()
        
        # Generate clickbait title
        print("Generating clickbait title...", flush=True)
        title = generate_clickbait_title(articles_data)
        print(f"Generated title: {title}", flush=True)
        
        # Update JSON with title
        print("Updating JSON with title...", flush=True)
        title = update_json_with_title(title)
        print("Added title to JSON", flush=True)
        
        # Generate SEO-optimized article content
        print("Generating SEO-optimized article content...", flush=True)
        article_content = generate_article_content(articles_data, title)
        
        # Save article as markdown
        with open('temp/final.md', 'w', encoding='utf-8') as f:
            f.write(article_content)
        print("SEO-optimized article saved as temp/final.md", flush=True)
        
        # Generate excerpt from the final article
        print("Generating excerpt...", flush=True)
        excerpt = generate_excerpt()
        
        # Get today's date
        print("Getting today's date...", flush=True)
        date = get_todays_date()
        
        # Categorize the article
        print("Categorizing article...", flush=True)
        category = categorize_article()
        
        # Update JSON with metadata
        print("Updating JSON with metadata...", flush=True)
        update_json_with_metadata(excerpt, date, category)
        
        # Get random image
        print("Selecting random image...", flush=True)
        source_image_path = get_random_image()
        print(f"Selected image: {source_image_path}", flush=True)
        
        # Generate new image
        print("Generating new image...", flush=True)
        new_image = generate_new_image(source_image_path)
        
        # Check if image generation was successful
        if new_image is None:
            print("Image generation failed. Skipping article creation.", flush=True)
            print("Article will be cleaned up later by clear_temp.py if needed.", flush=True)
            return
        
        # Resize image
        print("Resizing image...", flush=True)
        resized_image = resize_image(new_image)
        
        # Save final image
        resized_image.save('temp/final.jpg', 'JPEG', quality=95)
        print("Image saved as temp/final.jpg (1200x630 px)", flush=True)
        
        print("Content generation completed successfully!", flush=True)
        print(f"Final title: {title}", flush=True)
        
    except Exception as e:
        print(f"Error: {str(e)}", flush=True)

if __name__ == "__main__":
    main()