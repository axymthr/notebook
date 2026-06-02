#!/bin/bash
# 1. Set up your vault paths as variables
SRC_VAULT="Obsidian Vault"
DEST_VAULT="scratch vault"
SRC_DIR="$(obsidian vault="$SRC_VAULT" vault info=path)"
DEST_DIR="$(obsidian vault="$DEST_VAULT" vault info=path)"

# 1. Clear terminal output
echo "🚀 Initiating cross-vault copy..."

# 2. Find and copy files matching "Untitled*" while maintaining folder structure using native macOS utilities
# Using a null-terminated string (-print0) safely handles files with spaces in the name
#find "$SRC_DIR" -type f -name "Untitled*" | while read -r file; do
find "$SRC_DIR" -type f -name "Untitled*" -print0 | while IFS= read -r -d '' file; do
    # Calculate the target relative path to preserve subfolders
    rel_path="${file#$SRC_DIR/}"
    dest_file="$DEST_DIR/$rel_path"

    # Ensure any matching subfolder structure exists in the destination
    mkdir -p "$(dirname "$dest_file")"

    # Copy the file
    # Copy the actual file with content preserved
    cp "$file" "$dest_file"
    echo "✓ Copied: $rel_path"
done
echo "⚙️ Forcing Destination Vault to re-index..."

# 3. Use the Obsidian CLI to cleanly trigger a database reload
# This safely forces Obsidian to parse the new files without needing a manual app restart
obsidian vault="$DEST_VAULT" reload
