# Codebaser

## Overview

Codebaser is a repository containing tools and scripts designed to facilitate the indexing and understanding of codebases. These tools are intended to aid in navigating, analyzing, and managing large-scale code projects efficiently.

## Tools

### Flatten Codebase Script

`flatten_codebase.py` is a Python script that flattens a specified codebase by concatenating source code files from given directories. This tool ensures a structured output that is easily indexable and interpretable by both humans and language models.

#### Features

- Handles multiple file types and directories.
- Ensures that output is accessible and organized for further processing.
- Customizable to ignore non-text files and specific file extensions.

#### Usage

```bash
python flatten_codebase.py --folders path/to/folder1 path/to/folder2 --ext py,cpp,java
```
