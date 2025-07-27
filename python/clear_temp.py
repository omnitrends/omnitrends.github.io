#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clear all files in the temp folder.
This script removes all files from the temp directory while preserving the directory structure.
"""

import os
import shutil
import sys
import json
from pathlib import Path

# Fix Unicode output issues on Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


def clear_temp_folder():
    """Clear all files and subdirectories from the temp folder."""
    # Get the script's directory and navigate to temp folder
    script_dir = Path(__file__).parent
    temp_dir = script_dir.parent / "temp"
    
    if not temp_dir.exists():
        print(f"Temp directory does not exist: {temp_dir}")
        return
    
    print(f"Clearing temp folder: {temp_dir}")
    
    # Count files and directories before deletion
    files_count = 0
    dirs_count = 0
    
    try:
        for item in temp_dir.iterdir():
            if item.is_file():
                files_count += 1
                item.unlink()
                print(f"Deleted file: {item.name}")
            elif item.is_dir():
                dirs_count += 1
                shutil.rmtree(item)
                print(f"Deleted directory: {item.name}")
        
        print(f"\nTemp folder cleanup completed successfully!")
        print(f"Removed {files_count} files and {dirs_count} directories")
        
    except PermissionError as e:
        print(f"Permission error: {e}")
        print("Make sure the files are not in use and you have proper permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")


def cleanup_articles_without_images():
    """Remove HTML files from articles folder and corresponding entries from articles.json if no matching image exists in images folder."""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    articles_dir = project_root / "articles"
    images_dir = project_root / "images"
    articles_json_file = project_root / "json" / "articles.json"
    
    if not articles_dir.exists():
        print(f"Articles directory does not exist: {articles_dir}")
        return
    
    if not images_dir.exists():
        print(f"Images directory does not exist: {images_dir}")
        return
    
    if not articles_json_file.exists():
        print(f"articles.json file does not exist: {articles_json_file}")
        return
    
    print("Checking for articles without corresponding images...")
    
    try:
        # Load articles.json
        with open(articles_json_file, 'r', encoding='utf-8') as f:
            articles_data = json.load(f)
        
        # Get list of image files (without extensions)
        image_files = set()
        for image_file in images_dir.glob("*.webp"):
            image_files.add(image_file.stem)  # filename without extension
        
        # Get list of HTML files in articles directory
        html_files = list(articles_dir.glob("*.html"))
        
        removed_html_count = 0
        removed_json_entries = 0
        updated_articles_data = []
        
        # Check each article in articles.json
        for article in articles_data:
            article_id = article.get('id', '')
            
            # Check if corresponding image exists
            if article_id in image_files:
                # Image exists, keep the article
                updated_articles_data.append(article)
            else:
                # No corresponding image, mark for removal
                print(f"No image found for article ID: {article_id}")
                removed_json_entries += 1
                
                # Remove corresponding HTML file if it exists
                html_file = articles_dir / f"{article_id}.html"
                if html_file.exists():
                    html_file.unlink()
                    print(f"Removed HTML file: {html_file.name}")
                    removed_html_count += 1
        
        # Update articles.json with remaining articles
        if removed_json_entries > 0:
            with open(articles_json_file, 'w', encoding='utf-8') as f:
                json.dump(updated_articles_data, f, indent=2, ensure_ascii=False)
            print(f"Updated articles.json - removed {removed_json_entries} entries")
        
        print(f"Cleanup completed: Removed {removed_html_count} HTML files and {removed_json_entries} JSON entries")
        
    except Exception as e:
        print(f"Error during articles cleanup: {e}")


def clear_latest_trends_json():
    """Clear the content of the latest_trends.json file from the json folder."""
    # Get the script's directory and navigate to json folder
    script_dir = Path(__file__).parent
    json_dir = script_dir.parent / "json"
    latest_trends_file = json_dir / "latest_trends.json"
    
    if not json_dir.exists():
        print(f"JSON directory does not exist: {json_dir}")
        return
    
    if not latest_trends_file.exists():
        print(f"latest_trends.json file does not exist: {latest_trends_file}")
        return
    
    try:
        # Clear the content by writing an empty JSON object
        with open(latest_trends_file, 'w', encoding='utf-8') as f:
            f.write('{}')
        
        print(f"Cleared content of: {latest_trends_file}")
        print("latest_trends.json content cleared successfully!")
        
    except PermissionError as e:
        print(f"Permission error clearing latest_trends.json: {e}")
        print("Make sure the file is not in use and you have proper permissions.")
    except Exception as e:
        print(f"An error occurred while clearing latest_trends.json: {e}")


if __name__ == "__main__":
    # First cleanup articles without corresponding images
    cleanup_articles_without_images()
    print()  # Add spacing between functions
    
    # Then clear temp folder
    clear_temp_folder()
    print()  # Add spacing between functions
    
    # Finally clear latest trends
    clear_latest_trends_json()