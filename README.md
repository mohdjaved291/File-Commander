# Readme

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A modern command-line interface that interprets natural language commands to perform file operations. File Commander uses LiteLLM and OpenRouter to understand complex commands and execute file management tasks with minimal user effort.

## ✨ Features

- **Natural Language Command Processing**: Control your file system using everyday language
- **Multi-Step Operations**: Execute complex workflows with a single command
- **Beautiful Terminal UI**: Professional dark-themed interface with rich visual feedback
- **LiteLLM Integration**: Uses DeepSeek R1 through OpenRouter for advanced language understanding
- **Comprehensive File Operations**: Create, move, rename, search, and more
- **Media Playback**: Easily find and play media files with intelligent matching
- **Deep Path Understanding**: Intelligently resolves paths, common locations, and drives

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenRouter API key (free tier available)

## 🚀 Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/file-commander.git
cd file-commander
```

2. Create a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install required dependencies:

```bash
pip install typer rich python-dotenv litellm
```

4. Create a `.env` file in the project directory:

```
OPENROUTER_API_KEY=your-openrouter-api-key-here
```

## 🖥 Usage

File Commander uses a command-line interface for interaction:

```bash
# Process a natural language command
python file-commander.py command "Create folder reports on Desktop"

# Show help information
python file-commander.py help
```

## 🗣 Example Commands

### Basic File Operations

```bash
# Create folders
python file-commander.py command "Create folder project_files"
python file-commander.py command "Create a new folder called Meeting Notes"
python file-commander.py command "Make a directory named 2024_Projects in Documents"

# Create files
python file-commander.py command "Create file report.docx"
python file-commander.py command "Create a new file named budget.xlsx in Documents"

# Rename items
python file-commander.py command "Rename folder old_stuff to archive"
python file-commander.py command "Change folder name Projects to Completed_Projects"
```

### File Management

```bash
# Move files
python file-commander.py command "Move file document.txt to Documents"
python file-commander.py command "Move budget.xlsx from Desktop to Documents/Finance"

# Move multiple files
python file-commander.py command "Move all files from Desktop/backups to Downloads/archive"
```

### Navigation and Search

```bash
# Open file explorer
python file-commander.py command "Open file explorer in Downloads"
python file-commander.py command "Open file explorer in drive D"

# Search for files
python file-commander.py command "Search for budget files in Documents"
python file-commander.py command "Find files with report in the name in Downloads"
```

### Media Playback

```bash
# Play media files
python file-commander.py command "Play movie Inception"
python file-commander.py command "I want to watch The Matrix"
```

### Multi-Step Commands

File Commander now processes multiple operations in a single command:

```bash
# Create nested structures
python file-commander.py command "Create a folder called Projects on Desktop, create a folder called Development inside Projects, and create a file called readme.txt inside the Development folder"

# Organize files
python file-commander.py command "Create a folder called Backup on Desktop, move all files from Downloads to Backup, then create a file called backup_log.txt in the Backup folder"

# Complex workflows
python file-commander.py command "Search for files containing budget in Documents, then create a folder called Financial_Reports on Desktop and open file explorer in the Desktop folder"
```

## 🛠 Troubleshooting

- **Command not understood**: Try rephrasing using simpler language
- **Path errors**: Ensure paths exist and are correctly specified
- **Slow response**: The first command may take longer due to API initialization
- **API errors**: Check your OpenRouter API key and internet connection
- **JSON parsing errors**: If you see a warning about JSON parsing, retry the command
- **Multiple interpretations**: For ambiguous commands, be more specific

## 📜 License

This project is open-source and available under the MIT License.

## Acknowledgements

- LiteLLM for the unified LLM interface
- OpenRouter for providing access to powerful language models
- Typer for the command-line interface
- Rich for beautiful terminal output
- DeepSeek for their excellent open-source language models
