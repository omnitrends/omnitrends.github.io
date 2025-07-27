#!/usr/bin/env python3
"""
Clear all files in the temp folder.
This script removes all files from the temp directory while preserving the directory structure.
"""

import os
import shutil
from pathlib import Path


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
        
        print(f"\nCleanup completed successfully!")
        print(f"Removed {files_count} files and {dirs_count} directories")
        
    except PermissionError as e:
        print(f"Permission error: {e}")
        print("Make sure the files are not in use and you have proper permissions.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    clear_temp_folder()