#!/usr/bin/env python3
"""
Script to fetch images from GitHub using data.json
"""

import json
import os
import requests
from pathlib import Path

def fetch_images_from_json(json_file="data.json", output_dir="images"):
    """
    Fetch all images from GitHub using the data.json file
    
    Args:
        json_file: Path to the JSON file (default: data.json)
        output_dir: Directory to save images (default: images)
    """
    # Read the JSON file
    json_path = Path(json_file)
    if not json_path.exists():
        print(f"Error: {json_file} not found!")
        return False
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Get repo info
    username = data.get("username", "")
    repo = data.get("repo", "")
    branch = data.get("branch", "")
    
    print(f"Fetching images from GitHub: {username}/{repo}")
    print(f"Branch/Commit: {branch}")
    print("-" * 60)
    
    success_count = 0
    failed_count = 0
    
    for image in data["images"]:
        url = image["githubRawUrl"]
        image_name = image["name"]
        output_file = output_path / image_name
        
        try:
            print(f"Downloading {image_name}...", end=" ")
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Save the image
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content) / 1024  # KB
            print(f"✓ Saved to {output_file} ({file_size:.1f} KB)")
            success_count += 1
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Failed: {e}")
            failed_count += 1
        except Exception as e:
            print(f"✗ Error: {e}")
            failed_count += 1
    
    print("-" * 60)
    print(f"Summary: {success_count} succeeded, {failed_count} failed")
    
    return failed_count == 0


if __name__ == "__main__":
    import sys
    
    json_file = sys.argv[1] if len(sys.argv) > 1 else "data.json"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "images"
    
    success = fetch_images_from_json(json_file, output_dir)
    exit(0 if success else 1)
