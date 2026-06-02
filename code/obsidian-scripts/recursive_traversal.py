import os
import re
import shutil
from pathlib import Path

# Regex to capture the file target inside [[WikiLinks]] or ![[Embeds]]
LINK_REGEX = re.compile(r'!?\[\[([^\]|#]+)')


def find_root_notes(vault_path, tag="#extract"):
    """Finds all markdown files containing the initial target tag."""
    roots = []
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                path = Path(root) / file
                try:
                    if tag in path.read_text(encoding='utf-8'):
                        roots.append(path)
                except Exception:
                    continue
    return roots


def resolve_dependencies(current_note, vault_path, manifest, visited):
    """Recursively traces note links and assets to build a complete manifest."""
    if current_note in visited:
        return
    visited.add(current_note)
    manifest.add(current_note)

    try:
        content = current_note.read_text(encoding='utf-8')
    except Exception:
        return

    # Find all links and asset references in the current note
    links = LINK_REGEX.findall(content)

    for link in links:
        # Resolve Obsidian's short paths to an absolute system path
        dependency_path = locate_file_in_vault(vault_path, link)

        if dependency_path and dependency_path.exists():
            if dependency_path.suffix == '.md':
                # It's a linked note: recurse deeper down the graph
                resolve_dependencies(dependency_path, vault_path, manifest, visited)
            else:
                # It's an image or resource asset: add to manifest, no need to recurse
                manifest.add(dependency_path)


def locate_file_in_vault(vault_path, link_target):
    """
    Obsidian often uses shortest-path linking (e.g., [[image.png]] instead of [[assets/image.png]]).
    This helper finds the actual file on disk matching the link target name.
    """
    # If the link already contains an extension, use it; otherwise assume .md
    target_name = link_target if '.' in link_target else f"{link_target}.md"
    target_name = os.path.basename(target_name)  # Strip any partial folder paths for matching

    for root, _, files in os.walk(vault_path):
        if target_name in files:
            return Path(root) / target_name
    return None


def export_manifest(manifest, source_vault, target_vault):
    for src_path in manifest:
        # Determine the relative path from the source vault root
        relative_path = os.path.relpath(src_path, source_vault)
        dest_path = Path(target_vault) / relative_path

        # Create missing parent directories in the target vault if they don't exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(src_path, dest_path)
        print(f"Copied: {relative_path}")
