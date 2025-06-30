## Copy a single note
```commandline
# Copy entire vault
python3 copy_obsidian_notes.py /path/to/source/vault /path/to/dest/vault

# Copy specific notes
python3 copy_obsidian_notes.py /path/to/source/vault /path/to/dest/vault --notes "Note1.md" "Note2.md"
```

```commandline
#!/bin/bash
# Copy all markdown files and common attachment folders
rsync -av --include="*.md" --include="attachments/" --include="assets/" --include="files/" --exclude="*" "$1/" "$2/"
```

## Copy a folder of notes
```commandline
# Copy a specific folder
python3 copy_obsidian_folder.py "/path/to/source/vault" "/path/to/dest/vault" "Projects"

# Copy a nested folder
python3 copy_obsidian_folder.py "/path/to/source/vault" "/path/to/dest/vault" "Work/Meeting Notes"
```

What this script does:

Copies the entire folder structure - All files, subfolders, and nested content
Preserves folder hierarchy - Maintains the exact same organization in the destination
THIS DOESN'T WORK YET: Handles linked resources - Finds images and attachments referenced in the markdown files and copies them too
Merges safely - If the destination folder exists, it merges rather than overwriting
Reports progress - Shows you what's being copied and any issues

```commandline
# Simple folder copy with rsync
rsync -av "/path/to/source/vault/FolderName/" "/path/to/dest/vault/FolderName/"
```

