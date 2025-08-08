#!/usr/bin/env python3
"""
One-time script to fix multiple H1 tag issues in existing articles.
This script removes the duplicate H1 tag from article content while keeping
the H1 tag in the HTML template structure.

Author: OmniTrends
Date: 2025
"""

import os
import re
import glob
from pathlib import Path

def get_project_root():
    """Get the project root directory (parent of python directory)"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(script_dir)

def fix_article_h1_tags(file_path):
    """
    Fix H1 tag issues in a single article file by converting logo H1 to div.
    
    Args:
        file_path (str): Path to the HTML article file
        
    Returns:
        bool: True if file was modified, False otherwise
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        original_content = content
        modified = False
        
        # Fix 1: Convert logo H1 to div for SEO optimization
        # Handle various H1 patterns with possible whitespace and attributes
        logo_h1_patterns = [
            r'<h1[^>]*>\s*OmniTrends\s*</h1>',  # H1 with possible attributes and whitespace
            r'<h1>\s*OmniTrends\s*</h1>',       # Simple H1 with possible whitespace
        ]
        
        for pattern in logo_h1_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, '<div class="site-logo">OmniTrends</div>', content, flags=re.IGNORECASE)
                modified = True
                print(f"✅ Converted logo H1 to div in {os.path.basename(file_path)}")
                break
        
        # Fix 2: Remove any H1 tags from article body content (if they exist)
        article_body_pattern = r'(<div class="article__body">)(.*?)(</div>)'
        match = re.search(article_body_pattern, content, re.DOTALL)
        
        if match:
            article_body_content = match.group(2)
            h1_pattern = r'<h1[^>]*>.*?</h1>\s*'
            
            if re.search(h1_pattern, article_body_content, re.DOTALL):
                fixed_article_body = re.sub(h1_pattern, '', article_body_content, count=1, flags=re.DOTALL)
                content = content.replace(article_body_content, fixed_article_body)
                modified = True
                print(f"✅ Removed H1 from article body in {os.path.basename(file_path)}")
        
        # Write the fixed content back to the file if any changes were made
        if modified:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        else:
            return False
            
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Main function to fix H1 tag SEO issues in all articles in the articles folder"""
    project_root = get_project_root()
    articles_dir = os.path.join(project_root, 'articles')
    
    if not os.path.exists(articles_dir):
        print(f"Error: Articles directory not found at {articles_dir}")
        return
    
    # Get all HTML files in the articles directory
    html_files = glob.glob(os.path.join(articles_dir, '*.html'))
    
    if not html_files:
        print(f"No HTML files found in {articles_dir}")
        return
    
    print(f"Found {len(html_files)} HTML files to process...")
    print("-" * 60)
    
    fixed_count = 0
    skipped_count = 0
    error_count = 0
    
    for file_path in html_files:
        filename = os.path.basename(file_path)
        print(f"Processing: {filename}")
        
        try:
            if fix_article_h1_tags(file_path):
                print(f"✅ Fixed: {filename}")
                fixed_count += 1
            else:
                print(f"⏭️  Skipped: {filename} (no changes needed)")
                skipped_count += 1
        except Exception as e:
            print(f"❌ Error: {filename} - {e}")
            error_count += 1
        
        print()
    
    # Summary
    print("=" * 60)
    print("SUMMARY:")
    print(f"Total files processed: {len(html_files)}")
    print(f"Files fixed: {fixed_count}")
    print(f"Files skipped: {skipped_count}")
    print(f"Files with errors: {error_count}")
    print("=" * 60)
    
    if fixed_count > 0:
        print("✅ H1 tag SEO issues have been fixed in the articles!")
        print("The articles now have proper single H1 tag structure for better SEO.")
        print("Logo H1 tags have been converted to div elements.")
    else:
        print("ℹ️  No files needed fixing.")

if __name__ == "__main__":
    main()