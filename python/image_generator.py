import os
import json
import time
import sys
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def read_markdown_file(file_path):
    """
    Read the content of a markdown file.
    
    Args:
        file_path (str): Path to the markdown file
        
    Returns:
        str: Content of the markdown file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"Successfully read markdown file: {file_path}")
        return content
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None

def generate_image_prompt(article_content):
    """
    Generate an image prompt based on the article content using Gemini text generation.
    
    Args:
        article_content (str): Content of the article
        
    Returns:
        str: Generated image prompt
    """
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Create prompt for generating image description
        prompt = f"""
        Read the following article and understand what it is about. Then create a detailed image generation prompt for a 1200x630px image based on the article's content.
        
        STRICT REQUIREMENTS for the image:
        1. Must NOT contain human figures or human body parts or human hands/feet/fingers
        2. Must look natural and avoid any unnatural distortion
        3. Should be visually appealing and professional
        4. Should capture the essence and theme of the article
        
        You decide what the article is about and create an appropriate image prompt accordingly. Focus on objects, landscapes, abstract representations, or other non-human elements that relate to the article's topic.
        
        Article content:
        {article_content}
        
        Generate only the image prompt, nothing else. Make it detailed and specific for best results.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disables thinking
            ),
        )
        
        image_prompt = response.text.strip()
        print(f"Generated image prompt: {image_prompt}")
        return image_prompt
        
    except Exception as e:
        print(f"Error generating image prompt: {str(e)}")
        print("Exiting due to prompt generation failure.")
        sys.exit(1)

def generate_image(prompt):
    """
    Generate an image using Gemini image generation model.
    
    Args:
        prompt (str): Text prompt for image generation
        
    Returns:
        PIL.Image: Generated image object
    """
    try:
        # Initialize Gemini client
        client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
        
        # Add size specification to the prompt
        full_prompt = f"{prompt}. Image size: 1200x630 pixels, high quality, professional look."
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        # Extract image from response
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(f"Image generation response: {part.text}")
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                print("Image generated successfully")
                return image
                
        print("No image found in response")
        print("Exiting due to image generation failure.")
        sys.exit(1)
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        print("Exiting due to image generation failure.")
        sys.exit(1)

def save_image(image, output_path):
    """
    Save the generated image to the specified path.
    
    Args:
        image (PIL.Image): Image object to save
        output_path (str): Path where to save the image
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Resize image to exact requirements if needed
        if image.size != (1200, 630):
            image = image.resize((1200, 630), Image.Resampling.LANCZOS)
            print(f"Resized image to 1200x630 pixels")
        
        # Save as JPEG
        image.save(output_path, 'JPEG', quality=95)
        print(f"Image saved successfully to: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error saving image: {str(e)}")
        return False

def read_id_from_json(json_path):
    """
    Read the ID value from keyword_selection.json file.
    
    Args:
        json_path (str): Path to the JSON file
        
    Returns:
        str: ID value from the JSON file
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        id_value = data.get('id')
        print(f"Read ID from JSON: {id_value}")
        return id_value
        
    except Exception as e:
        print(f"Error reading ID from JSON: {str(e)}")
        return None

def update_keyword_selection_json(json_path, id_value):
    """
    Update the keyword_selection.json file with image and featured keys.
    
    Args:
        json_path (str): Path to the JSON file
        id_value (str): ID value to use for the image filename
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read existing JSON data
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Add image key after date and before url
        # Add featured key after excerpt (at the end)
        data['image'] = f"{id_value}.webp"
        data['featured'] = True
        
        # Reorder keys to match the required structure
        ordered_data = {}
        for key in ['id', 'keyword', 'title', 'category', 'date', 'image', 'url', 'excerpt', 'featured']:
            if key in data:
                ordered_data[key] = data[key]
        
        # Write updated JSON data
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(ordered_data, file, indent=2, ensure_ascii=False)
        
        print(f"Updated JSON file with image: {id_value}.webp and featured: true")
        return True
        
    except Exception as e:
        print(f"Error updating JSON file: {str(e)}")
        return False

def main():
    """
    Main function to orchestrate the image generation process.
    """
    # File paths
    markdown_path = os.path.join(PROJECT_ROOT, 'temp', 'final.md')
    json_path = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
    output_image_path = os.path.join(PROJECT_ROOT, 'temp', 'final.jpg')
    
    print("Starting image generation process...")
    
    # Step 1: Read markdown file
    article_content = read_markdown_file(markdown_path)
    if not article_content:
        print("Failed to read markdown file. Exiting.")
        return
    
    # Step 2: Generate image prompt using Gemini
    image_prompt = generate_image_prompt(article_content)
    if not image_prompt:
        print("Failed to generate image prompt. Exiting.")
        sys.exit(1)
    
    # Wait 30 seconds before next API call
    print("Waiting 30 seconds before image generation...")
    time.sleep(30)
    
    # Step 3: Generate image using Gemini
    generated_image = generate_image(image_prompt)
    if not generated_image:
        print("Failed to generate image. Exiting.")
        sys.exit(1)
    
    # Step 4: Save image
    if not save_image(generated_image, output_image_path):
        print("Failed to save image. Exiting.")
        return
    
    # Step 5: Read ID from JSON
    id_value = read_id_from_json(json_path)
    if not id_value:
        print("Failed to read ID from JSON. Exiting.")
        return
    
    # Step 6: Update JSON file
    if not update_keyword_selection_json(json_path, id_value):
        print("Failed to update JSON file. Exiting.")
        return
    
    print("Image generation process completed successfully!")

if __name__ == "__main__":
    main()