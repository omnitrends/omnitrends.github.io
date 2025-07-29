import json
import os
import sys

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (parent of python directory)
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def load_json_file(file_path):
    """Load and return JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {file_path}.")
        sys.exit(1)

def save_json_file(file_path, data):
    """Save data to a JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        print(f"Successfully saved keyword selection to {file_path}")
    except Exception as e:
        print(f"Error saving file {file_path}: {e}")
        sys.exit(1)

def main():
    # Define file paths using PROJECT_ROOT
    trends_file = os.path.join(PROJECT_ROOT, 'temp', 'latest_trends.json')
    articles_file = os.path.join(PROJECT_ROOT, 'json', 'articles.json')
    output_file = os.path.join(PROJECT_ROOT, 'temp', 'keyword_selection.json')
    
    # Load latest trends
    print("Loading latest trends...")
    trends_data = load_json_file(trends_file)
    
    # Load existing articles
    print("Loading existing articles...")
    articles_data = load_json_file(articles_file)
    
    # Extract existing keywords from articles.json
    existing_keywords = set()
    for article in articles_data:
        if 'keyword' in article:
            existing_keywords.add(article['keyword'].lower())
    
    print(f"Found {len(existing_keywords)} existing keywords in articles.json")
    
    # Sort trends by rank and check each one
    trends = trends_data.get('trends', [])
    trends_sorted = sorted(trends, key=lambda x: x.get('rank', float('inf')))
    
    print(f"Checking {len(trends_sorted)} trends starting from rank 1...")
    
    # Find the first trend that doesn't match any existing keyword
    for trend in trends_sorted:
        trend_name = trend.get('trend_name', '').lower()
        rank = trend.get('rank')
        
        print(f"Checking rank {rank}: '{trend['trend_name']}'")
        
        # Check if this trend_name matches any existing keyword
        if trend_name not in existing_keywords:
            # Found a trend that doesn't match any existing keyword
            print(f"✓ Found unmatched trend at rank {rank}: '{trend['trend_name']}'")
            
            # Create the output data
            output_data = {
                "keyword": trend['trend_name']
            }
            
            # Save to keyword_selection.json
            save_json_file(output_file, output_data)
            print("Program completed successfully.")
            sys.exit(0)
        else:
            print(f"  → Skipping (matches existing keyword)")
    
    # If we reach here, no unmatched trend was found
    print("No unmatched trends found. All trends already have corresponding articles.")
    sys.exit(1)

if __name__ == "__main__":
    main()