#!/bin/bash
# Script to fetch images from GitHub using data.json

JSON_FILE="${1:-data.json}"
OUTPUT_DIR="${2:-images}"

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Install it with: brew install jq (macOS) or apt-get install jq (Linux)"
    exit 1
fi

# Check if JSON file exists
if [ ! -f "$JSON_FILE" ]; then
    echo "Error: $JSON_FILE not found!"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Fetching images from GitHub..."
echo "----------------------------------------"

# Read each image URL and download
jq -r '.images[] | "\(.name)|\(.githubRawUrl)"' "$JSON_FILE" | while IFS='|' read -r name url; do
    echo -n "Downloading $name... "
    
    if curl -s -f -L -o "$OUTPUT_DIR/$name" "$url"; then
        size=$(du -h "$OUTPUT_DIR/$name" | cut -f1)
        echo "✓ Saved to $OUTPUT_DIR/$name ($size)"
    else
        echo "✗ Failed to download"
    fi
done

echo "----------------------------------------"
echo "Done!"
