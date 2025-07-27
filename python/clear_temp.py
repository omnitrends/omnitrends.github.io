#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clear all files in the temp folder.
This script removes all files from the temp directory while preserving the directory structure.
"""

import os
import shutil
import sys
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
    clear_temp_folder()
    print()  # Add spacing between functions
    clear_latest_trends_json()