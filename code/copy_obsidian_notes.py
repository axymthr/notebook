#!/usr/bin/env python3
"""
Obsidian Vault Copy Script for macOS
Copies markdown notes and their linked attachments between vaults

# Copy entire vault
python3 copy_obsidian_notes.py /path/to/source/vault /path/to/dest/vault

# Copy specific notes
python3 copy_obsidian_notes.py /path/to/source/vault /path/to/dest/vault --notes "Note1.md" "Note2.md"
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
            
            # Try to find the actual file
            potential_paths = [
                os.path.join(source_vault_path, resource_path),
                os.path.join(source_vault_path, 'attachments', resource_path),
                os.path.join(source_vault_path, 'assets', resource_path),
                os.path.join(source_vault_path, 'files', resource_path),
            ]
            
            for potential_path in potential_paths:
                if os.path.exists(potential_path):
                    resources.add(potential_path)
                    break
    
    return resources

def copy_notes_with_resources(source_path, dest_path, notes_list=None):
    """Copy notes and their linked resources"""
    source_path = Path(source_path)
    dest_path = Path(dest_path)
    
    # Create destination directory if it doesn't exist
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # If no specific notes provided, copy all markdown files
    if notes_list is None:
        notes_list = list(source_path.rglob('*.md'))
    else:
        notes_list = [source_path / note for note in notes_list]
    
    copied_resources = set()
    
    for note_path in notes_list:
        if not note_path.exists():
            print(f"Warning: {note_path} not found")
            continue
            
        print(f"Processing: {note_path.name}")
        
        # Read the markdown content
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find linked resources
        resources = find_linked_resources(content, str(source_path))
        
        # Copy the note itself
        relative_path = note_path.relative_to(source_path)
        dest_note_path = dest_path / relative_path
        dest_note_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(note_path, dest_note_path)
        
        # Copy linked resources
        for resource_path in resources:
            if resource_path not in copied_resources:
                resource_path_obj = Path(resource_path)
                relative_resource = resource_path_obj.relative_to(source_path)
                dest_resource_path = dest_path / relative_resource
                dest_resource_path.parent.mkdir(parents=True, exist_ok=True)
                
                try:
                    shutil.copy2(resource_path, dest_resource_path)
                    copied_resources.add(resource_path)
                    print(f"  Copied resource: {relative_resource}")
                except Exception as e:
                    print(f"  Error copying {relative_resource}: {e}")
    
    print(f"\nCopied {len(notes_list)} notes and {len(copied_resources)} resources")

def main():
    parser = argparse.ArgumentParser(description='Copy Obsidian notes with linked resources')
    parser.add_argument('source', help='Source vault path')
    parser.add_argument('dest', help='Destination vault path')
    parser.add_argument('--notes', nargs='*', help='Specific notes to copy (optional)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"Error: Source path {args.source} does not exist")
        return
    
    copy_notes_with_resources(args.source, args.dest, args.notes)

if __name__ == '__main__':
    main()