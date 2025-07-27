#!/usr/bin/env python3
"""
Main script to run all content generation scripts in sequence.
Executes: trends_check.py -> search_articles.py -> content_generator.py -> html_generator.py -> clear_temp.py -> sitemap_generator.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_script(script_name):
    """Run a Python script and handle errors."""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ Error: {script_name} not found!")
        return False
    
    print(f"🚀 Running {script_name}...")
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        if result.stdout:
            print(f"📝 Output from {script_name}:")
            print(result.stdout)
        
        print(f"✅ {script_name} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected error running {script_name}: {str(e)}")
        return False

def main():
    """Main function to run all scripts in sequence."""
    print("🔄 Starting content generation pipeline...")
    print("=" * 50)
    
    scripts = [
        "trends_check.py",
        "search_articles.py", 
        "content_generator.py",
        "html_generator.py",
        "clear_temp.py",
        "sitemap_generator.py"
    ]
    
    successful_scripts = 0
    failed_scripts = []
    
    for script in scripts:
        print(f"\n{'='*20} {script} {'='*20}")
        
        if run_script(script):
            successful_scripts += 1
        else:
            failed_scripts.append(script)
            print(f"⚠️  Continuing with next script despite {script} failure...")
    
    print(f"\n{'='*50}")
    print("📊 Pipeline Summary:")
    print(f"✅ Successful: {successful_scripts}/{len(scripts)} scripts")
    
    if failed_scripts:
        print(f"❌ Failed scripts: {', '.join(failed_scripts)}")
        print("\n🔄 Pipeline completed with errors.")
        return 1
    else:
        print("🎉 All scripts completed successfully!")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)