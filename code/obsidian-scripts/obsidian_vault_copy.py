#!/usr/bin/env python3
"""
Obsidian Vault Copy Script
Copies notes between Obsidian vaults with dependency graph traversal.

Usage:
    python obsidian_vault_copy.py config.yaml
"""

import os
import sys
import yaml
import shutil
import re
from pathlib import Path
from datetime import datetime
from typing import Set, Dict, List, Optional, Tuple
from collections import deque


class ObsidianVaultCopier:
    """Handles copying notes between Obsidian vaults with link traversal."""
    
    def __init__(self, config_path: str):
        """Initialize with config file path."""
        self.config = self._load_config(config_path)
        self.source_vault = Path(self.config['source_vault']).expanduser().resolve()
        self.target_vault = Path(self.config['target_vault']).expanduser().resolve()
        self.copied_files: Set[Path] = set()
        self.target_path_overrides: Dict[Path, Path] = {}
        
        # Validate vaults exist
        if not self.source_vault.exists():
            raise ValueError(f"Source vault does not exist: {self.source_vault}")
        if not self.target_vault.exists():
            raise ValueError(f"Target vault does not exist: {self.target_vault}")
    
    def _load_config(self, config_path: str) -> dict:
        """Load and validate YAML config."""
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        required = ['source_vault', 'target_vault']
        for key in required:
            if key not in config:
                raise ValueError(f"Config missing required key: {key}")
        
        return config
    
    def _parse_wikilinks(self, content: str) -> List[str]:
        """Extract Obsidian wikilinks from note content."""
        # Match [[link]] and [[link|alias]] patterns
        pattern = r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        matches = re.findall(pattern, content)
        
        # Clean up links (remove anchors and handle special cases)
        links = []
        for match in matches:
            # Remove anchor fragments
            link = match.split('#')[0].strip()
            if link:
                links.append(link)
        
        return links
    
    def _parse_markdown_links(self, content: str) -> List[str]:
        """Extract markdown-style links to other notes."""
        # Match [text](path.md) patterns
        pattern = r'\[([^\]]+)\]\(([^)]+\.md)\)'
        matches = re.findall(pattern, content)
        
        links = []
        for _, link in matches:
            # Remove URL fragments and handle relative paths
            link = link.split('#')[0].strip()
            if not link.startswith('http://') and not link.startswith('https://'):
                links.append(link)
        
        return links
    
    def _parse_embeds(self, content: str) -> List[str]:
        """Extract embedded files (images, PDFs, etc)."""
        # Match ![[embed]] patterns
        pattern = r'!\[\[([^\]|]+)(?:\|[^\]]+)?\]\]'
        matches = re.findall(pattern, content)
        
        embeds = []
        for match in matches:
            embed = match.split('#')[0].strip()
            if embed:
                embeds.append(embed)
        
        return embeds
    
    def _resolve_note_path(self, link: str, current_note_dir: Path) -> Optional[Path]:
        """
        Resolve a note link to its actual file path in the vault.
        Obsidian searches the entire vault for note names.
        """
        # If it has an extension, treat as relative path
        if '.' in link:
            # Try relative to current note first
            relative_path = current_note_dir / link
            if relative_path.exists():
                return relative_path.relative_to(self.source_vault)
            
            # Try from vault root
            vault_path = self.source_vault / link
            if vault_path.exists():
                return Path(link)
        
        # No extension - Obsidian wikilink style
        # Search for .md file with this name anywhere in vault
        link_with_ext = f"{link}.md"
        
        # Try current directory first
        local_path = current_note_dir / link_with_ext
        if local_path.exists():
            return local_path.relative_to(self.source_vault)
        
        # Search entire vault
        for md_file in self.source_vault.rglob(link_with_ext):
            return md_file.relative_to(self.source_vault)
        
        # Try as-is (for attachments without extensions in wikilinks)
        for any_file in self.source_vault.rglob(link):
            return any_file.relative_to(self.source_vault)
        
        return None
    
    def _get_target_path(self, source_rel_path: Path) -> Path:
        """Get target path for a source file, respecting overrides."""
        if source_rel_path in self.target_path_overrides:
            return self.target_path_overrides[source_rel_path]
        return source_rel_path
    
    def _copy_file(self, source_rel_path: Path, target_rel_path: Optional[Path] = None) -> bool:
        """
        Copy a single file from source to target vault.
        Returns True if copied, False if skipped.
        """
        source_abs = self.source_vault / source_rel_path
        
        if not source_abs.exists():
            print(f"⚠️  Source file not found: {source_rel_path}")
            return False
        
        # Determine target path
        if target_rel_path is None:
            target_rel_path = source_rel_path
        
        target_abs = self.target_vault / target_rel_path
        
        # Create parent directories (like mkdir -p)
        target_abs.parent.mkdir(parents=True, exist_ok=True)
        
        # Handle file conflicts by appending timestamp
        if target_abs.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            stem = target_abs.stem
            suffix = target_abs.suffix
            target_abs = target_abs.parent / f"{stem}_{timestamp}{suffix}"
            print(f"⚠️  File exists, renaming to: {target_abs.name}")
        
        # Use shutil.copy2 to preserve metadata
        shutil.copy2(source_abs, target_abs)
        print(f"✓ Copied: {source_rel_path} → {target_abs.relative_to(self.target_vault)}")
        
        return True
    
    def _copy_with_dependencies(self, source_rel_path: Path, target_rel_path: Optional[Path] = None):
        """
        Copy a note and all its linked dependencies (graph traversal).
        Uses BFS to traverse the link graph.
        """
        # Queue for BFS: (source_path, target_path_override)
        queue = deque([(source_rel_path, target_rel_path)])
        visited: Set[Path] = set()
        
        while queue:
            current_source, current_target = queue.popleft()
            
            # Skip if already processed
            if current_source in visited:
                continue
            
            visited.add(current_source)
            
            # Copy the file
            if not self._copy_file(current_source, current_target):
                continue
            
            self.copied_files.add(current_source)
            
            # Only parse links if it's a markdown file
            current_abs = self.source_vault / current_source
            if current_abs.suffix.lower() not in ['.md', '.markdown']:
                continue
            
            # Read file and extract links
            try:
                with open(current_abs, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"⚠️  Could not read {current_source}: {e}")
                continue
            
            # Extract all types of links
            wikilinks = self._parse_wikilinks(content)
            md_links = self._parse_markdown_links(content)
            embeds = self._parse_embeds(content)
            
            all_links = wikilinks + md_links + embeds
            
            # Resolve and queue dependencies
            current_note_dir = (self.source_vault / current_source).parent
            
            for link in all_links:
                resolved = self._resolve_note_path(link, current_note_dir)
                
                if resolved is None:
                    print(f"⚠️  Could not resolve link: {link} (from {current_source})")
                    continue
                
                if resolved in visited:
                    continue
                
                # Check if there's an override for this linked file
                linked_target = self.target_path_overrides.get(resolved, None)
                
                queue.append((resolved, linked_target))
    
    def run(self):
        """Execute the copy operation based on config."""
        print(f"Source vault: {self.source_vault}")
        print(f"Target vault: {self.target_vault}")
        print()
        
        # Process target path overrides
        if 'target_paths' in self.config:
            for source, target in self.config['target_paths'].items():
                source_path = Path(source)
                target_path = Path(target)
                self.target_path_overrides[source_path] = target_path
        
        # Process individual notes
        if 'notes' in self.config:
            print("Copying individual notes...")
            for note_config in self.config['notes']:
                if isinstance(note_config, str):
                    source_path = Path(note_config)
                    target_path = None
                elif isinstance(note_config, dict):
                    source_path = Path(note_config['source'])
                    target_path = Path(note_config['target']) if 'target' in note_config else None
                else:
                    print(f"⚠️  Invalid note config: {note_config}")
                    continue
                
                print(f"\nProcessing: {source_path}")
                self._copy_with_dependencies(source_path, target_path)
        
        # Process folders
        if 'folders' in self.config:
            print("\nCopying folders...")
            for folder_config in self.config['folders']:
                if isinstance(folder_config, str):
                    source_folder = Path(folder_config)
                    target_folder = None
                elif isinstance(folder_config, dict):
                    source_folder = Path(folder_config['source'])
                    target_folder = Path(folder_config['target']) if 'target' in folder_config else None
                else:
                    print(f"⚠️  Invalid folder config: {folder_config}")
                    continue
                
                print(f"\nProcessing folder: {source_folder}")
                source_abs = self.source_vault / source_folder
                
                if not source_abs.exists() or not source_abs.is_dir():
                    print(f"⚠️  Folder not found: {source_folder}")
                    continue
                
                # Find all markdown files in folder
                for md_file in source_abs.rglob('*.md'):
                    rel_path = md_file.relative_to(self.source_vault)
                    
                    # Calculate target path if folder target is specified
                    if target_folder:
                        rel_to_folder = md_file.relative_to(source_abs)
                        file_target = target_folder / rel_to_folder
                    else:
                        file_target = None
                    
                    print(f"\nProcessing: {rel_path}")
                    self._copy_with_dependencies(rel_path, file_target)
        
        print(f"\n✅ Done! Copied {len(self.copied_files)} files.")


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: python obsidian_vault_copy.py config.yaml")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    if not os.path.exists(config_path):
        print(f"Error: Config file not found: {config_path}")
        sys.exit(1)
    
    try:
        copier = ObsidianVaultCopier(config_path)
        copier.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
