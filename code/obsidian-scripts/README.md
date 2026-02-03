# Obsidian Vault Copy Script

A Python script to copy notes between Obsidian vaults with automatic dependency graph traversal.

## Architecture Evaluation

### Python vs Node.js vs Split Approach

**Winner: Single Python Script ✅**

#### Why Python?
1. **Excellent file system operations**: Python's `pathlib` and `shutil` are perfect for this task
2. **Simple deployment**: Single file, works with standard macOS Python 3
3. **YAML parsing**: Built-in with PyYAML
4. **Regex support**: Native and powerful for parsing Obsidian links
5. **Graph traversal**: Collections module (deque) is perfect for BFS

#### Why NOT Node.js?
- Would require node_modules and package.json
- No significant benefit for file operations
- More setup complexity for end users
- Python's pathlib > Node's path module for this use case

#### Why NOT split into vault script + Python?
- Adds unnecessary complexity
- Obsidian doesn't have a JS API for vault plugins that would help here
- Python can do everything in one pass efficiently
- Single script is easier to maintain and use

### About Using `cp` Command

The script **does NOT delegate to `cp`** for these reasons:

1. **Graph traversal**: `cp` can't follow Obsidian wikilinks
2. **Link resolution**: Need to parse markdown and resolve Obsidian's link syntax
3. **Conflict handling**: Need timestamp-based renaming
4. **Selective copying**: Need to respect YAML config and overrides

The script uses `shutil.copy2()` which:
- Preserves metadata (like `cp -p`)
- Is cross-platform
- Integrates cleanly with Python's Path operations

## Features

### Story 1: Basic Copy ✅
- Copy individual notes with relative paths
- Copy entire folders recursively
- Specify custom target paths for notes and folders
- Automatic directory creation (like `mkdir -p`)
- Timestamp-based conflict resolution
- Preserves file metadata

### Story 2: Advanced Graph Traversal ✅
- Parses Obsidian wikilinks: `[[Note Name]]`
- Parses wikilinks with aliases: `[[Note Name|Display]]`
- Parses markdown links: `[text](note.md)`
- Parses embedded files: `![[image.png]]`
- Resolves links across entire vault (Obsidian's search behavior)
- BFS graph traversal to copy all dependencies
- Respects target path overrides for dependencies
- Handles circular references automatically

## Installation

### Requirements
- Python 3.7+
- PyYAML library

### Setup
```bash
# Install PyYAML
pip3 install pyyaml

# Make script executable
chmod +x obsidian_vault_copy.py
```

## Usage

### 1. Create Config File
Create a `config.yaml` file next to the script:

```yaml
# Source and target vault locations (required)
source_vault: ~/Documents/MyVault
target_vault: ~/Documents/BackupVault

# Individual notes to copy
notes:
  - "Projects/Project A.md"
  - source: "Research/Paper.md"
    target: "Archive/Papers/Paper.md"

# Folders to copy
folders:
  - "Meeting Notes"
  - source: "Personal/Journal"
    target: "Archive/Journal"

# Optional path overrides
target_paths:
  "Templates/Template1.md": "System/Templates/Template1.md"
```

### 2. Run Script
```bash
python3 obsidian_vault_copy.py config.yaml
```

## How It Works

### Graph Traversal Algorithm
Yes, this is a **graph traversal problem**. The script uses **Breadth-First Search (BFS)**:

1. Start with notes/folders specified in config
2. Copy the note to target vault
3. Parse the note for all links (wikilinks, markdown links, embeds)
4. Resolve each link to its actual file path
5. Add resolved files to the queue
6. Repeat until queue is empty

**Why BFS?**
- Ensures closest dependencies are copied first
- Prevents infinite loops (visited set)
- Efficient for broad dependency graphs
- Natural for this use case

### Link Resolution
Obsidian's link resolution is complex:
1. Try relative to current note
2. Try relative to vault root
3. Search entire vault for matching filename
4. Handle extensions (.md is optional in wikilinks)

The script mimics this behavior to find all linked notes.

### Conflict Handling
- Files already existing in target vault are NOT overwritten
- New copies get timestamp suffix: `Note_20240115_143022.md`
- Directories are created automatically as needed

## Config File Format

### Required Fields
```yaml
source_vault: /path/to/source/vault
target_vault: /path/to/target/vault
```

### Optional Fields

#### Individual Notes
```yaml
notes:
  # Simple - copy to same path
  - "Folder/Note.md"
  
  # With custom target
  - source: "Source/Note.md"
    target: "Target/Note.md"
```

#### Folders
```yaml
folders:
  # Simple - copy folder contents to same path
  - "Folder Name"
  
  # With custom target
  - source: "Source Folder"
    target: "Target Folder"
```

#### Target Path Overrides
```yaml
target_paths:
  "source/relative/path.md": "target/relative/path.md"
  "attachments/img.png": "media/img.png"
```

These override where specific files go when encountered as dependencies.

## Examples

### Example 1: Basic Copy
```yaml
source_vault: ~/Obsidian/MainVault
target_vault: ~/Obsidian/Archive

notes:
  - "2024/January Review.md"
  - "Projects/Completed/Project X.md"
```

### Example 2: Reorganize Structure
```yaml
source_vault: ~/Obsidian/MainVault
target_vault: ~/Obsidian/CleanVault

notes:
  - source: "Inbox/Idea 1.md"
    target: "Ideas/2024/Idea 1.md"

folders:
  - source: "Old Projects"
    target: "Archive/Projects"
```

### Example 3: Copy with Dependencies
```yaml
source_vault: ~/Obsidian/Work
target_vault: ~/Obsidian/Portfolio

notes:
  - "Projects/Major Project.md"  # Will copy all linked notes!

# Override where templates go
target_paths:
  "Templates/Project Template.md": "System/Templates/Project.md"
```

## Troubleshooting

### "Source vault does not exist"
- Check the path in config.yaml
- Use absolute paths or ~ for home directory
- Ensure no typos

### "Could not resolve link"
- The linked note doesn't exist in source vault
- This is a warning, not an error
- Script continues copying other files

### "File exists, renaming"
- Target file already exists
- New file gets timestamp: `Note_20240115_143022.md`
- Original target file is preserved

### Script doesn't find dependencies
- Ensure links use Obsidian syntax: `[[Note]]` or `[text](note.md)`
- Check that linked files exist in source vault
- Wikilinks are case-sensitive in file resolution

## Performance

- **Fast**: Uses native file operations
- **Memory efficient**: BFS with visited set prevents redundant processing
- **Safe**: No file overwrites, only copies

For large vaults (1000+ notes), expect:
- ~1-2 seconds per 100 notes
- Primarily limited by disk I/O
- Graph traversal is O(V + E) where V=notes, E=links

## Limitations

1. Does not modify link paths in copied notes (preserves original links)
2. Does not copy vault settings or plugins
3. Does not handle broken links (warns but continues)
4. Does not support all possible Obsidian link formats (edge cases)

## Future Enhancements

Possible additions:
- Rewrite links to match new structure
- Copy .obsidian folder settings
- Support for Dataview queries
- Dry-run mode to preview changes
- Progress bar for large vaults
- Exclude patterns (ignore certain folders/files)

## License

MIT License - Use freely for personal or commercial projects.
