#!/usr/bin/env python3
"""
Obsidian Folder Copy Script for macOS
Copies a complete folder from one vault to another, including all linked resources

# Copy a specific folder
python3 copy_obsidian_folder.py "/path/to/source/vault" "/path/to/dest/vault" "Projects"

# Copy a nested folder
python3 copy_obsidian_folder.py "/path/to/source/vault" "/path/to/dest/vault" "Work/Meeting Notes"
"""

import os
import re
import shutil
import argparse
from pathlib import Path

def find_linked_resources(markdown_content, source_vault_path):
    """Find all linked resources in a markdown file"""
    resources = set()
    
    # Pattern for markdown images: ![alt](path) and ![[wikilink]]
    img_patterns = [
        r'!\[.*?\]\(([^)]+)\)',  # ![alt](path)
        r'!\[\[([^\]]+)\]\]',    # ![[wikilink]]
    ]
    
    # Pattern for embedded files: [[file.pdf]] or [text](file.pdf)
    file_patterns = [
        r'\[\[([^\]]+\.(pdf|docx?|xlsx?|pptx?|zip|mp4|mov|mp3|wav))\]\]',
        r'\[.*?\]\(([^)]+\.(pdf|docx?|xlsx?|pptx?|zip|mp4|mov|mp3|wav))\)',
    ]
    
    all_patterns = img_patterns + [p[0] for p in file_patterns]
    
    for pattern in all_patterns:
        matches = re.findall(pattern, markdown_content, re.IGNORECASE)
        for match in matches:
            if isinstance(match, tuple):
                resource_path = match[0]
            else:
                resource_path = match
            
            # Clean up the path
            resource_path = resource_path.strip()
            if resource_path.startswith('./'):
                resource_path = resource_path[2:]
            
            # Try to find the actual file in common attachment locations
            potential_paths = [
                os.path.join(source_vault_path, resource_path),
                os.path.join(source_vault_path, 'attachments', resource_path),
                os.path.join(source_vault_path, 'assets', resource_path),
                os.path.join(source_vault_path, 'files', resource_path),
                os.path.join(source_vault_path, '_resources', resource_path),
            ]
            
            for potential_path in potential_paths:
                if os.path.exists(potential_path):
                    resources.add(potential_path)
                    break
    
    return resources

def copy_folder_with_resources(source_vault_path, dest_vault_path, folder_name):
    """Copy a complete folder and its linked resources between vaults"""
    source_vault = Path(source_vault_path)
    dest_vault = Path(dest_vault_path)
    source_folder = source_vault / folder_name
    dest_folder = dest_vault / folder_name
    
    # Check if source folder exists
    if not source_folder.exists():
        print(f"Error: Folder '{folder_name}' not found in source vault")
        return
    
    # Create destination vault directory if it doesn't exist
    dest_vault.mkdir(parents=True, exist_ok=True)
    
    print(f"Copying folder: {folder_name}")
    print(f"From: {source_folder}")
    print(f"To: {dest_folder}")
    
    # Copy the entire folder structure first
    if dest_folder.exists():
        print(f"Destination folder exists, merging contents...")
    
    shutil.copytree(source_folder, dest_folder, dirs_exist_ok=True)
    print(f"✓ Copied folder structure and all files")
    
    # Now find and copy any external linked resources
    copied_resources = set()
    markdown_files = list(source_folder.rglob('*.md'))
    
    print(f"Scanning {len(markdown_files)} markdown files for linked resources...")
    
    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            resources = find_linked_resources(content, str(source_vault))
            
            for resource_path in resources:
                # Skip resources that are already inside the folder we copied
                if not str(resource_path).startswith(str(source_folder)):
                    if resource_path not in copied_resources:
                        resource_path_obj = Path(resource_path)
                        relative_resource = resource_path_obj.relative_to(source_vault)
                        dest_resource_path = dest_vault / relative_resource
                        dest_resource_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        try:
                            shutil.copy2(resource_path, dest_resource_path)
                            copied_resources.add(resource_path)
                            print(f"  ✓ Copied external resource: {relative_resource}")
                        except Exception as e:
                            print(f"  ✗ Error copying {relative_resource}: {e}")
        
        except Exception as e:
            print(f"  Warning: Could not process {md_file.name}: {e}")
    
    if copied_resources:
        print(f"✓ Copied {len(copied_resources)} external linked resources")
    else:
        print("✓ No external linked resources found")
    
    print(f"\n🎉 Successfully copied folder '{folder_name}' to destination vault!")

def main():
    parser = argparse.ArgumentParser(description='Copy a complete folder from one Obsidian vault to another')
    parser.add_argument('source_vault', help='Source vault path')
    parser.add_argument('dest_vault', help='Destination vault path')
    parser.add_argument('folder_name', help='Name of folder to copy')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source_vault):
        print(f"Error: Source vault {args.source_vault} does not exist")
        return
    
    copy_folder_with_resources(args.source_vault, args.dest_vault, args.folder_name)

if __name__ == '__main__':
    main()