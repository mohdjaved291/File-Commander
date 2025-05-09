#!/usr/bin/env python3
"""
File Commander - Modern Natural Language File Management

A command-line application that uses natural language to perform file operations.
Built with Typer, LiteLLM, and Rich for a beautiful and intuitive interface.
"""

import os
import shutil
import subprocess
import re
import json
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from rich.table import Table
from dotenv import load_dotenv

# Initialize Typer app and Rich console
app = typer.Typer(help="File Commander - Natural language file management")
console = Console()

# Load environment variables
load_dotenv()

# Directory paths
HOME_DIR = os.path.expanduser("~")
DESKTOP_DIR = os.path.join(HOME_DIR, "Desktop")
DOWNLOADS_DIR = os.path.join(HOME_DIR, "Downloads")
DOCUMENTS_DIR = os.path.join(HOME_DIR, "Documents")
PICTURES_DIR = os.path.join(HOME_DIR, "Pictures")
MUSIC_DIR = os.path.join(HOME_DIR, "Music")
VIDEOS_DIR = os.path.join(HOME_DIR, "Videos")
MOVIES_DIR = os.path.join("D:", "Movies") if os.name == 'nt' else os.path.join(HOME_DIR, "Movies")

# Create a mapping of common locations
COMMON_LOCATIONS = {
    "home": HOME_DIR,
    "desktop": DESKTOP_DIR,
    "downloads": DOWNLOADS_DIR,
    "documents": DOCUMENTS_DIR,
    "pictures": PICTURES_DIR,
    "music": MUSIC_DIR,
    "videos": VIDEOS_DIR,
    "movies": MOVIES_DIR,
    # Add common variations
    "docs": DOCUMENTS_DIR,
    "my documents": DOCUMENTS_DIR,
    "my desktop": DESKTOP_DIR,
    "my downloads": DOWNLOADS_DIR,
    "pics": PICTURES_DIR,
    "photos": PICTURES_DIR,
}

# Add drive letters if on Windows
if os.name == 'nt':
    for drive_letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{drive_letter}:\\"
        if os.path.exists(drive_path):
            COMMON_LOCATIONS[f"drive_{drive_letter.lower()}"] = drive_path
            COMMON_LOCATIONS[f"{drive_letter.lower()}_drive"] = drive_path
            COMMON_LOCATIONS[f"{drive_letter.lower()}"] = drive_path
            COMMON_LOCATIONS[f"drive {drive_letter.lower()}"] = drive_path


class FileOperations:
    """Core file operation functionality."""
    
    def __init__(self):
        self.current_path = os.path.expanduser("~")
        self.video_extensions = [
            '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', 
            '.m4v', '.mpg', '.mpeg', '.3gp', '.3g2', '.m2ts'
        ]
    
    def resolve_path(self, path: str) -> str:
        """Resolve a path string to an absolute path."""
        if not path:
            return self.current_path
        
        path = path.strip()
        
        # Quick return for absolute paths
        if os.path.isabs(path):
            return path
        
        # Check common paths
        if path.lower() in COMMON_LOCATIONS:
            return COMMON_LOCATIONS[path.lower()]
        
        # Special handling for drive references (Windows)
        drive_match = re.match(r"^(?:drive\s+)?([a-zA-Z])[:\s]?$", path)
        if drive_match:
            drive_letter = drive_match.group(1).lower()
            drive_path = f"{drive_letter.upper()}:\\"
            if os.path.exists(drive_path):
                return drive_path
        
        # Check if it has a drive letter (Windows)
        if len(path) > 1 and path[0].isalpha() and path[1] == ':':
            return path
        
        # Normalize the path
        return os.path.normpath(os.path.join(self.current_path, path))
    
    def create_folder(self, folder_name: str, location: str = "") -> str:
        """Create a new folder at the specified location."""
        folder_name = folder_name.strip()
        
        # Resolve the base path
        base_path = self.resolve_path(location) if location else self.current_path
        
        # Create full folder path
        folder_path = os.path.join(base_path, folder_name)
        
        try:
            # Check if folder already exists
            if os.path.exists(folder_path):
                return f"Folder already exists: {folder_path}"
            
            # Create the folder
            os.makedirs(folder_path)
            return f"Created folder: {folder_path}"
        except Exception as e:
            return f"Error creating folder: {str(e)}"
    
    def create_file(self, file_name: str, location: str = "", content: str = "") -> str:
        """Create a new file at the specified location."""
        file_name = file_name.strip()
        
        # Resolve the base path
        base_path = self.resolve_path(location) if location else self.current_path
        
        # Create full file path
        file_path = os.path.join(base_path, file_name)
        
        try:
            # Check if file already exists
            if os.path.exists(file_path):
                return f"File already exists: {file_path}"
            
            # Create the file
            with open(file_path, 'w') as f:
                if content:
                    f.write(content)
            
            return f"Created file: {file_path}"
        except Exception as e:
            return f"Error creating file: {str(e)}"
    
    def rename_item(self, old_name: str, new_name: str, location: str = "") -> str:
        """Rename a file or folder."""
        # Resolve the base path
        base_path = self.resolve_path(location) if location else self.current_path
        
        # Create full paths
        old_path = os.path.join(base_path, old_name)
        new_path = os.path.join(base_path, new_name)
        
        try:
            # Check if source exists
            if not os.path.exists(old_path):
                return f"Source does not exist: {old_path}"
            
            # Check if destination already exists
            if os.path.exists(new_path):
                return f"Destination already exists: {new_path}"
            
            # Rename the item
            os.rename(old_path, new_path)
            return f"Renamed from {old_path} to {new_path}"
        except Exception as e:
            return f"Error renaming item: {str(e)}"
    
    def move_item(self, source: str, destination: str) -> str:
        """Move a file or folder to a new location."""
        try:
            # Resolve paths
            source_path = self.resolve_path(source)
            dest_path = self.resolve_path(destination)
            
            # Check if source exists
            if not os.path.exists(source_path):
                return f"Source does not exist: {source_path}"
            
            # If destination is a directory, move inside it
            if os.path.isdir(dest_path):
                dest_path = os.path.join(dest_path, os.path.basename(source_path))
            
            # Check if destination already exists
            if os.path.exists(dest_path):
                return f"Destination already exists: {dest_path}"
            
            # Move the item
            shutil.move(source_path, dest_path)
            return f"Moved from {source_path} to {dest_path}"
        except Exception as e:
            return f"Error moving item: {str(e)}"
    
    def move_all_files(self, source_dir: str, destination_dir: str) -> str:
        """Move all files from source directory to destination directory."""
        try:
            # Resolve paths
            source_path = self.resolve_path(source_dir)
            dest_path = self.resolve_path(destination_dir)
            
            # Check if source exists and is a directory
            if not os.path.exists(source_path):
                return f"Source directory does not exist: {source_path}"
            
            if not os.path.isdir(source_path):
                return f"Source is not a directory: {source_path}"
            
            # Check if destination exists and is a directory
            if not os.path.exists(dest_path):
                return f"Destination directory does not exist: {dest_path}"
            
            if not os.path.isdir(dest_path):
                return f"Destination is not a directory: {dest_path}"
            
            # Count files to move
            files_to_move = [f for f in os.listdir(source_path) 
                            if os.path.isfile(os.path.join(source_path, f))]
            
            if not files_to_move:
                return f"No files found in the source directory: {source_path}"
            
            # Move all files
            moved_files = 0
            skipped_files = 0
            
            for file in track(files_to_move, description="Moving files"):
                source_file = os.path.join(source_path, file)
                dest_file = os.path.join(dest_path, file)
                
                if os.path.exists(dest_file):
                    # Skip files that already exist in destination
                    skipped_files += 1
                    continue
                    
                # Move the file
                shutil.move(source_file, dest_file)
                moved_files += 1
            
            # Generate result message
            result = f"Moved {moved_files} files from {source_path} to {dest_path}"
            if skipped_files > 0:
                result += f"\nSkipped {skipped_files} files that already exist in the destination."
            
            return result
        
        except Exception as e:
            return f"Error moving files: {str(e)}"
    
    def open_file_explorer(self, location: str = "") -> str:
        """Open file explorer at the specified location."""
        try:
            # Resolve the path
            path_to_open = self.resolve_path(location) if location else self.current_path
            
            # Check if the path exists
            if not os.path.exists(path_to_open):
                return f"Location does not exist: {path_to_open}"
            
            # Open file explorer at the path
            if os.name == 'nt':  # Windows
                subprocess.Popen(f'explorer "{path_to_open}"', shell=True)
            elif os.name == 'posix':  # macOS/Linux
                if os.path.exists('/usr/bin/open'):  # macOS
                    subprocess.Popen(['open', path_to_open])
                else:  # Linux
                    subprocess.Popen(['xdg-open', path_to_open])
            
            return f"Opened file explorer at: {path_to_open}"
        except Exception as e:
            return f"Error opening file explorer: {str(e)}"
    
    def search_files(self, search_term: str, search_path: str = "") -> str:
        """Search for files containing the search term."""
        if not search_term:
            return "No search term specified."
        
        try:
            # Resolve the path
            base_path = self.resolve_path(search_path) if search_path else self.current_path
            
            # Check if the path exists
            if not os.path.exists(base_path):
                return f"Search location does not exist: {base_path}"
            
            # Search for files
            found_files = []
            max_files = 10
            
            for root, _, files in os.walk(base_path):
                if len(found_files) >= max_files:
                    break
                
                # Add matching files to the list
                for file in files:
                    if search_term.lower() in file.lower():
                        found_files.append(os.path.join(root, file))
                        if len(found_files) >= max_files:
                            break
            
            # Process results
            if not found_files:
                return f"No files found containing '{search_term}' in {base_path}"
            
            # Create a table for results
            table = Table(title=f"Search Results for '{search_term}'", show_header=True)
            table.add_column("#", style="dim")
            table.add_column("File Name", style="green")
            table.add_column("Path", style="blue")
            
            for i, path in enumerate(found_files, 1):
                file_name = os.path.basename(path)
                dir_name = os.path.dirname(path)
                table.add_row(str(i), file_name, dir_name)
            
            console.print(table)
            return f"Found {len(found_files)} files containing '{search_term}'"
            
        except Exception as e:
            return f"Error searching files: {str(e)}"
    
    def play_movie(self, movie_name: str) -> str:
        """Search for and play a movie with the default media player."""
        if not movie_name:
            return "No movie name specified."
        
        try:
            # Check if the movies directory exists
            movies_dir = COMMON_LOCATIONS.get("movies")
            if not os.path.exists(movies_dir):
                return f"Movies directory does not exist: {movies_dir}"
            
            # Find movies matching the name
            found_movies = []
            
            for root, _, files in os.walk(movies_dir):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in self.video_extensions):
                        file_lower = file.lower()
                        movie_lower = movie_name.lower()
                        
                        # Calculate a simple match score
                        score = 0
                        if movie_lower in file_lower:
                            score += 50
                        
                        # Check individual words
                        movie_words = movie_lower.split()
                        for word in movie_words:
                            if word in file_lower:
                                score += 10
                        
                        if score > 0:
                            full_path = os.path.join(root, file)
                            found_movies.append((full_path, score))
            
            if not found_movies:
                return f"No movie found with name '{movie_name}'"
            
            # Sort by match score (higher is better)
            found_movies.sort(key=lambda x: x[1], reverse=True)
            
            # Get the best match
            best_match_path = found_movies[0][0]
            
            # Open the movie with default player
            if os.name == 'nt':  # Windows
                os.startfile(best_match_path)
            elif os.name == 'posix':  # macOS/Linux
                if os.path.exists('/usr/bin/open'):  # macOS
                    subprocess.Popen(['open', best_match_path])
                else:  # Linux
                    subprocess.Popen(['xdg-open', best_match_path])
            
            return f"Playing movie: {os.path.basename(best_match_path)}"
        except Exception as e:
            return f"Error playing movie: {str(e)}"


# Initialize FileOperations
file_ops = FileOperations()

# Command processor using LiteLLM
class CommandProcessor:
    """Process natural language commands using LiteLLM."""
    
    def __init__(self, model_name="openrouter/deepseek/deepseek-r1"):
        """Initialize the command processor with OpenRouter via LiteLLM."""
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not self.api_key:
            console.print("[bold red]Error: OPENROUTER_API_KEY not set in environment variables.[/]")
            console.print("Please add your OpenRouter API key to the .env file.")
            return None
        
        # Set up environment variables for LiteLLM
        os.environ["OPENROUTER_API_KEY"] = self.api_key
        
        # Import LiteLLM here to ensure environment variables are set first
        try:
            import litellm
            self.litellm = litellm
            self.model_name = model_name
        except ImportError:
            console.print("[bold red]Error: LiteLLM package not installed.[/]")
            console.print("Please install it with: pip install litellm")
            self.litellm = None
    
    def parse_command(self, command: str) -> dict:
        """Parse a natural language command using LiteLLM."""
        if not self.litellm:
            return {"operation": "unknown", "parameters": {}}
    
        try:
            # Format the prompt with support for sequential operations
            system_message = """
            You are a file system command interpreter. Parse the natural language command below into a structured format.
        
            Based on the command, identify the operation(s) and parameters. The possible operations are:
            1. create_folder - Parameters: folder_name, location (optional)
            2. create_file - Parameters: file_name, location (optional), content (optional)
            3. rename_item - Parameters: old_name, new_name, location (optional)
            4. move_item - Parameters: source, destination
            5. move_all_files - Parameters: source_dir, destination_dir
            6. open_file_explorer - Parameters: location (optional)
            7. search_files - Parameters: search_term, search_path (optional)
            8. play_movie - Parameters: movie_name
        
            The command may contain multiple operations that need to be performed in sequence.
            If it's a single operation, output a JSON object with the operation and parameters:
            {"operation": "create_folder", "parameters": {"folder_name": "reports", "location": "Desktop"}}
        
            If the command contains multiple sequential operations, output a JSON object with an "operations" array:
            {
                "has_multiple_operations": true,
                "operations": [
                    {"operation": "create_folder", "parameters": {"folder_name": "movies", "location": "Desktop"}},
                    {"operation": "create_folder", "parameters": {"folder_name": "hollywood", "location": "Desktop/movies"}}
                ]
            }
        
            If the command is unclear, return:
            {"operation": "unknown", "parameters": {}}
        
            Always return only the JSON without any markdown formatting or code blocks.
            """
        
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Command: {command}"}
            ]
        
            # Call LiteLLM to get the response
            response = self.litellm.completion(
                model=self.model_name,
                messages=messages,
                temperature=0
            )
        
            # Extract the content from the response
            content = response.choices[0].message.content
        
            # Clean the response - remove markdown code blocks if present
            cleaned_content = self._clean_json_response(content)
        
            # Parse the JSON response
            try:
                result = json.loads(cleaned_content)
                return result
            except json.JSONDecodeError:
                console.print("[bold yellow]Warning: Could not parse JSON response from LLM.[/]")
                console.print(f"Response: {content}")
                return {"operation": "unknown", "parameters": {}}
            
        except Exception as e:
            console.print(f"[bold red]Error processing command with LiteLLM: {str(e)}[/]")
            return {"operation": "unknown", "parameters": {}}
    
    def _clean_json_response(self, content):
        """Clean the JSON response by removing markdown code blocks."""
        # Remove markdown code block syntax if present
        if "```" in content:
            # Extract content between code fences
            import re
            match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", content)
            if match:
                return match.group(1).strip()
    
        # If no code blocks found, return the original content
        return content

# Main command interface
@app.command()
def command(
    cmd: str = typer.Argument(..., help="Natural language command")
):
    """Process a natural language command."""
    # Display fancy header
    header = Text("File Commander", style="bold blue")
    console.print(Panel(header, subtitle="Natural Language File Management"))
    
    # Display the command
    console.print(f"[bold cyan]Command:[/] {cmd}")
    
    try:
        # Initialize command processor
        processor = CommandProcessor()
        
        # Process the command
        with console.status("[bold green]Processing command...[/]") as status:
            result = processor.parse_command(cmd)
            
            # Check if we have multiple operations
            if result.get("has_multiple_operations"):
                operations = result.get("operations", [])
                
                if not operations:
                    console.print("[bold yellow]No valid operations found in the command.[/]")
                    return
                
                # Process each operation in sequence
                outputs = []
                for op_data in operations:
                    operation = op_data.get("operation")
                    parameters = op_data.get("parameters", {})
                    
                    # Execute the operation
                    output = execute_operation(operation, parameters)
                    outputs.append(output)
                
                # Display all outputs
                for i, output in enumerate(outputs, 1):
                    console.print(f"[bold green]Step {i}:[/] {output}")
            else:
                # Process single operation
                operation = result.get("operation")
                parameters = result.get("parameters", {})
                
                # Execute the operation
                output = execute_operation(operation, parameters)
                
                # Display the output
                console.print("[bold green]Result:[/]", output)
    
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")


def execute_operation(operation, parameters):
    """Execute a single operation based on the operation type and parameters."""
    if operation == "create_folder":
        folder_name = parameters.get("folder_name", "")
        location = parameters.get("location", "")
        return file_ops.create_folder(folder_name, location)
    
    elif operation == "create_file":
        file_name = parameters.get("file_name", "")
        location = parameters.get("location", "")
        content = parameters.get("content", "")
        return file_ops.create_file(file_name, location, content)
    
    elif operation == "rename_item":
        old_name = parameters.get("old_name", "")
        new_name = parameters.get("new_name", "")
        location = parameters.get("location", "")
        return file_ops.rename_item(old_name, new_name, location)
    
    elif operation == "move_item":
        source = parameters.get("source", "")
        destination = parameters.get("destination", "")
        return file_ops.move_item(source, destination)
    
    elif operation == "move_all_files":
        source_dir = parameters.get("source_dir", "")
        destination_dir = parameters.get("destination_dir", "")
        return file_ops.move_all_files(source_dir, destination_dir)
    
    elif operation == "open_file_explorer":
        location = parameters.get("location", "")
        return file_ops.open_file_explorer(location)
    
    elif operation == "search_files":
        search_term = parameters.get("search_term", "")
        search_path = parameters.get("search_path", "")
        return file_ops.search_files(search_term, search_path)
    
    elif operation == "play_movie":
        movie_name = parameters.get("movie_name", "")
        return file_ops.play_movie(movie_name)
    
    else:
        return "Sorry, I couldn't understand that command. Please try again."

@app.command()
def help():
    """Display help information about File Commander."""
    console.print(Panel.fit(
        "[bold]File Commander[/]\n\n"
        "A natural language file management tool that lets you control your files and folders using everyday language.\n\n"
        "[bold cyan]Example commands:[/]\n"
        "- Create folder reports on Desktop\n"
        "- Move document.txt from Downloads to Documents\n"
        "- Open file explorer in drive D\n"
        "- Play movie Inception\n"
        "- Search for budget files in Documents\n"
        "- Rename folder old_stuff to archive\n",
        title="Help", border_style="green"
    ))


if __name__ == "__main__":
    app()