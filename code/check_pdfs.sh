#!/bin/bash

# Usage: ./check_pdfs.sh <source_dir> <target_dir>

if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_directory> <target_directory>"
    echo "Example: $0 /path/to/source /path/to/target"
    exit 1
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

# Check if directories exist
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory '$TARGET_DIR' does not exist"
    exit 1
fi

# Find all PDF files in source directory
find "$SOURCE_DIR" -name "*.pdf" -type f | while read -r source_file; do
    # Get just the filename
    filename=$(basename "$source_file")
    
    # Get the size of the source file
    source_size=$(stat -f%z "$source_file" 2>/dev/null)
    
    # Check if file exists in target directory
    target_file="$TARGET_DIR/$filename"
    
    if [ -f "$target_file" ]; then
        # File exists, check size
        target_size=$(stat -f%z "$target_file" 2>/dev/null)
        
        if [ "$source_size" != "$target_size" ]; then
            echo "Size mismatch: $filename (source: $source_size bytes, target: $target_size bytes)"
        fi
    else
        # File doesn't exist in target
        echo "Missing: $filename ($source_size bytes)"
    fi
done