import os
from pathlib import Path
from typing import List, Set

def get_folder_name_without_extension(path: str) -> str:
    """Extract folder name without extension."""
    print(os.path.basename(Path(path)))
    print(Path(path).name)
    return f'{Path(path).parent.name}_{Path(path).name}'

def generate_index_html(directory: str) -> None:
    """
    Generate index.html file for the given directory.
    Includes links to subfolders and files.
    """
    # Get absolute paths
    abs_path = os.path.abspath(directory)
    parent_path = os.path.dirname(abs_path)
    
    # Create index.html content
    html_content = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "    <meta charset='UTF-8'>",
        "    <title>Directory Listing</title>",
        "    <style>",
        "        body { font-family: Arial, sans-serif; margin: 20px; }",
        "        .nav-link { display: block; margin: 10px 0; }",
        "        .file-link { display: block; margin: 5px 0; }",
        "        .folder { color: blue; }",
        "        .file { color: black; }",
        "    </style>",
        "</head>",
        "<body>"
    ]
    
    # Add navigation to parent directory if not root
    if parent_path != abs_path:
        html_content.extend([
            "    <a href='../' class='nav-link'>Parent Directory</a>",
            "    <hr>"
        ])
    
    # Process subfolders
    subfolders = []
    files = []
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            subfolders.append(item)
        elif os.path.isfile(item_path):
            files.append(item)
    
    # Add subfolder links
    if subfolders:
        html_content.extend(["    <h2>Folders:</h2>"])
        for folder in sorted(subfolders):
            html_content.extend([
                f"    <a href='{folder}/' class='nav-link folder'>{folder}</a>"
            ])
    
    # Add file links
    if files:
        html_content.extend(["    <h2>Files:</h2>"])
        for file in sorted(files):
            html_content.extend([
                f"    <a href='{file}' class='file-link file'>{get_folder_name_without_extension(file)}</a>"
            ])
    
    # Close HTML tags
    html_content.extend([
        "    <hr>",
        "    <small>Generated automatically</small>",
        "</body>",
        "</html>"
    ])
    
    # Write to index.html
    index_path = os.path.join(directory, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_content))

def process_directory_tree(start_dir: str) -> None:
    """
    Recursively process directory tree, generating index.html files where needed.
    """
    for root, dirs, _ in os.walk(start_dir):
        # Skip if directory already has index.html
        #if 'index.html' in os.listdir(root):
        #    continue
            
        # Generate index.html for this directory
        generate_index_html(root)

if __name__ == "__main__":
    # Start from current directory
    current_dir = os.getcwd()
    print(f"Generating index.html files starting from: {current_dir}")
    process_directory_tree(current_dir)
