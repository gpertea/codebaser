#!/bin/env python
## this requires python 3
import os
import argparse

def is_text_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            if b'\0' in f.read(1024):
                return False
        return True
    except Exception:
        return False

def has_valid_extension(filename, extensions):
    # Check for specific 'makefile' names case insensitively
    if filename.lower() in ['makefile']:
        return True
    # Check for specified extensions
    return any(filename.lower().endswith('.' + ext.lower()) for ext in extensions)

def print_folder_structure(directory, output_file, output_filepath):
    # Include the directory directly in the header
    directory_header = directory if directory != '.' else '.'
    output_file.write(f"#~[DIR_TREE] {directory_header}\n")
    root_length = len(directory) if directory != '.' else 0  # To avoid cutting off the first character if it's '.'
    for root, directories, files in os.walk(directory):
        # Adjust the level to not redundantly list the base folder
        level = root[root_length:].count(os.sep)
        findent='';
        indent=''
        if level>0:
          indent = '  ' * (level-1)  # Using 2 spaces per level
          findent = '  ' * level
          display_root = root[root_length:].lstrip('/')  # Strip leading '/' to avoid leading spaces
          output_file.write(f"{indent}{os.path.basename(display_root)}/\n")        
        for f in files:
            file_path = os.path.join(root, f)
            if os.path.getsize(file_path) > 0 and os.path.abspath(file_path) != output_filepath:
                output_file.write(f"{findent}{f}\n")

def walk_folder_tree(folder, valid_extensions, output_filepath):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            # Exclude the output file from being added to the output
            if os.path.abspath(filepath) == output_filepath or os.path.getsize(filepath) == 0:
                continue
            #if is_text_file(filepath) and has_valid_extension(filename, valid_extensions):
            if has_valid_extension(filename, valid_extensions):
                yield filepath

def main():
    parser = argparse.ArgumentParser(description='Flattens a codebase with specified file extensions, including all Makefiles, excluding output file.')
    parser.add_argument('--folders', nargs='*', help='Base folders to process')
    parser.add_argument('--llm', action='store_true', help='Print instructions for language model to understand the flattened codebase file structure')
    parser.add_argument('--ext', nargs='*', help='List of file extensions to include', 
                        default=['c', 'cpp', 'hpp', 'h', 'hh', 'py', 'pl', 'sh', 'txt', 'md', 'R', 'Rmd'])
    args = parser.parse_args()

    llm_instructions = """
## LLM Instructions for Assistance in Codebase Understanding

### Role Definition:
- **Act as a software engineer** tasked with assisting in understanding and navigating a codebase.
- Provide insights, explanations, and solutions based on the provided codebase information.

### Codebase File Structure:
- The output text file uses a structured format to represent the directory structure and the contents of files.
- The directory tree is introduced by '#~[DIR_TREE] directory_path' line, listing directories and files hierarchically:
  #~[DIR_TREE] directory_path
    file.ext
    subdirectory/
      file.ext 
      subdirectory/
         file.ext
- Each file content is marked with a `#~[FILE] relative_file_path` line, where relative_file_path is the path of
  each file, relative to the directory_path of the last #~[DIR_TREE] line, followed by the actual content of the file:
  #~[FILE] relative_file_path
  ...verbatim content of the file...
- These tagged sections provide a clear structure for distinguishing between directory layouts and file contents, facilitating easy navigation and understanding of the codebase.

### Guidelines for Interaction:
- Respond to queries based on the explicit content and tags provided within the text file.
- Avoid making assumptions about the code without clear evidence presented in the tags and content.
- Reference specific files or directory paths using the exact tags presented, ensuring accurate and context-specific responses.
"""
    if args.llm:
        print(llm_instructions)
        return
    output_filename = 'codebase.txt'
    output_filepath = os.path.abspath(output_filename)

    base_folders = [folder.rstrip('/') for folder in args.folders]  # Trim trailing slashes

    valid_extensions = args.ext

    with open(output_filename, 'w') as output_file:
        for base_folder in base_folders:
            # Adjust the print and walk functions to exclude the output file path
            print_folder_structure(base_folder, output_file, output_filepath)
            for filepath in walk_folder_tree(base_folder, valid_extensions, output_filepath):
                normalized_path = filepath.replace('./', '') if base_folder == '.' else filepath
                output_file.write(f"#~[FILE] {normalized_path}\n")
                with open(filepath, "r") as f:
                    output_file.write(f.read() + "\n")

if __name__ == "__main__":
    main()
