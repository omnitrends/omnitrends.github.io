import json
import os

def count_articles():
    """Count the number of elements in articles.json"""
    # Get the path to articles.json relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, '..', 'json', 'articles.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as file:
            articles = json.load(file)
            
        # Count the number of articles
        count = len(articles)
        print(f"Number of articles in articles.json: {count}")
        return count
        
    except FileNotFoundError:
        print("Error: articles.json file not found!")
        return 0
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in articles.json!")
        return 0
    except Exception as e:
        print(f"Error reading articles.json: {e}")
        return 0

if __name__ == "__main__":
    count_articles()