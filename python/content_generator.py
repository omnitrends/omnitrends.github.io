import json
import glob
import random
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import PIL.Image

# Load environment variables
load_dotenv()

def load_articles():
    """Load articles from article_analysis.json"""
    with open('temp/article_analysis.json', 'r', encoding='utf-8') as f:
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
    
    prompt = f"""Create an eye-catching, clickbait title for an article about "{trend_topic}" that uses dark psychology principles to make Indian readers feel compelled to click. 

CRITICAL REQUIREMENT: The title MUST contain the exact keyword "{trend_topic}" somewhere in it.

Use these psychological triggers:
- Fear of missing out (FOMO)
- Curiosity gap (incomplete information that makes people want to know more)
- Social proof (what others are doing/saying)
- Urgency (time-sensitive language)
- Exclusivity (insider information, secrets)
- Emotional triggers (shocking, surprising, controversial)

The title should be:
- Maximum 60 characters for SEO
- Target Indian audience specifically
- Use simple, conversational English
- Include power words like "Shocking", "Secret", "Revealed", "You Won't Believe", etc.
- Make it sound urgent and exclusive
- MUST include the exact keyword "{trend_topic}" in the title

Examples of good clickbait titles (replace [Topic] with "{trend_topic}"):
- "This Shocking Truth About {trend_topic} Will Change Everything for Indians"
- "Secret Revealed: What Indians Don't Know About {trend_topic}"
- "You Won't Believe What Happened with {trend_topic} - Indian Perspective"

Generate only the title, nothing else. Remember: The title MUST contain "{trend_topic}"."""

    response = model.generate_content(prompt)
    
    print("Waiting 60 seconds before next API call...")
    time.sleep(60)
    
    return response.text.strip().title()

def update_json_with_title(title):
    """Update article_analysis.json with generated title"""
    with open('temp/article_analysis.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Add title to each article
    for article in data['articles']:
        article['gemini_title'] = title
    
    # Save updated JSON
    with open('temp/article_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
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
    
    prompt = f"""Create a highly SEO-optimized, human-sounding article for Indian readers about "{trend_topic}". Use the title "{title}" as H1.

REQUIREMENTS:
1. Write in simple, conversational English that Indians understand easily
2. Target Indian audience specifically with local context and references
3. Make it sound completely human-written, not AI-generated
4. 300-350 words total
5. Structure for Google Discover and AdSense approval
6. Use proper markdown formatting with headers (H1, H2, H3)

STRUCTURE (in markdown):
# {title}

## Introduction (2-3 sentences explaining why this matters to Indians)

## Key Points (2-3 H3 subheadings with content)
### First Key Point
### Second Key Point  
### Third Key Point (if needed)

## What This Means for Indians
(Explain local impact, relevance to Indian audience)

## Conclusion
(Wrap up with actionable insights or future implications)

SEO REQUIREMENTS:
- Use the main keyword "{trend_topic}" naturally 3-4 times
- Include related keywords naturally
- Write engaging meta-worthy content
- Use short paragraphs (2-3 sentences max)
- Include questions to engage readers
- Make it shareable and discussion-worthy

TONE:
- Conversational and friendly
- Informative but not boring
- Relatable to middle-class Indian families
- Avoid complex jargon
- Use common Indian English expressions

Based on these articles:
{combined_text}

Generate ONLY the markdown article content, no explanations or meta-text."""

    response = model.generate_content(prompt)
    
    print("Waiting 60 seconds before next API call...")
    time.sleep(60)
    
    return response.text

def get_random_image():
    """Get a random image from temp folder"""
    image_patterns = ['temp/*.png', 'temp/*.jpg', 'temp/*.jpeg']
    all_images = []
    
    for pattern in image_patterns:
        all_images.extend(glob.glob(pattern))
    
    if not all_images:
        raise FileNotFoundError("No images found in temp folder")
    
    return random.choice(all_images)

def generate_new_image(source_image_path):
    """Generate a new image using Gemini image-to-image generation"""
    from google import genai
    from google.genai import types
    
    # Configure Gemini client with API key
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    
    client = genai.Client(api_key=gemini_api_key)
    
    # Load the source image
    image = PIL.Image.open(source_image_path)
    
    # Create a prompt for image generation with specific instructions for human figures
    text_input = ('Transform this image into a modern, dynamic sports-themed image. '
                 'Add vibrant colors, energy, and a professional look suitable for a sports article. '
                 'Make it visually appealing and engaging for football fans. '
                 'IMPORTANT: If there are human figures in the image, maintain proper human anatomy - '
                 'keep all body parts in correct proportions, do not distort faces, hands, feet, or limbs. '
                 'Preserve natural human body structure and proportions. '
                 'Focus on enhancing colors, lighting, and background while keeping people looking realistic and natural.',)
    
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[text_input, image],
        config=types.GenerateContentConfig(
            response_modalities=['TEXT', 'IMAGE']
        )
    )
    
    # Extract the generated image
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            generated_image = Image.open(BytesIO((part.inline_data.data)))
            return generated_image
    
    raise Exception("No image generated")

def resize_image(image, target_size=(1200, 630)):
    """Resize image to target dimensions"""
    return image.resize(target_size, Image.Resampling.LANCZOS)

def main():
    try:
        # Load articles data
        print("Loading articles...")
        articles_data = load_articles()
        
        # Generate clickbait title
        print("Generating clickbait title...")
        title = generate_clickbait_title(articles_data)
        print(f"Generated title: {title}")
        
        # Update JSON with title
        print("Updating JSON with title...")
        title = update_json_with_title(title)
        print("Added title to JSON")
        
        # Generate SEO-optimized article content
        print("Generating SEO-optimized article content...")
        article_content = generate_article_content(articles_data, title)
        
        # Save article as markdown
        with open('temp/final.md', 'w', encoding='utf-8') as f:
            f.write(article_content)
        print("SEO-optimized article saved as temp/final.md")
        
        # Get random image
        print("Selecting random image...")
        source_image_path = get_random_image()
        print(f"Selected image: {source_image_path}")
        
        # Generate new image
        print("Generating new image...")
        new_image = generate_new_image(source_image_path)
        
        # Resize image
        print("Resizing image...")
        resized_image = resize_image(new_image)
        
        # Save final image
        resized_image.save('temp/final.jpg', 'JPEG', quality=95)
        print("Image saved as temp/final.jpg (1200x630 px)")
        
        print("Content generation completed successfully!")
        print(f"Final title: {title}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()