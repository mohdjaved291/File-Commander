import speech_recognition as sr
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import os
import webbrowser


class SpeechRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Recognition App")
        self.root.geometry("800x600")
        
        # Set theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors and styles
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 10), background='#f0f0f0')
        style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'), background='#f0f0f0')
        
        # Initialize variables
        self.is_listening = False
        self.listen_thread = None
        self.search_web = False
        
        # Create UI
        self.create_ui()
        
        # Configure recognizer
        self.setup_recognizer()
        
        # Welcome message
        self.add_text("Welcome to Speech Recognition App with Web Search!\n\n")
        self.add_text("1. Click 'Start Listening' and speak clearly\n")
        self.add_text("2. Your speech will be transcribed below\n")
        self.add_text("3. Enable 'Search Web' to automatically search for what you say\n\n")

    def setup_recognizer(self):
        """Set up the speech recognizer with appropriate settings"""
        try:
            self.recognizer = sr.Recognizer()
            
            # Sensitivity settings
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.6
            
            # Use default microphone
            self.microphone = sr.Microphone()
            self.mic_working = True
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize speech recognizer: {str(e)}")

    def create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(
            main_frame, text="Speech Recognition App", style='Header.TLabel'
        )
        title_label.pack(pady=(0, 15))

        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Engine selection
        ttk.Label(controls_frame, text="Engine:").pack(side=tk.LEFT, padx=(0, 5))
        self.engine_var = tk.StringVar(value="google")
        engines = ["google", "sphinx"]
        ttk.Combobox(
            controls_frame,
            textvariable=self.engine_var,
            values=engines,
            state="readonly",
            width=10,
        ).pack(side=tk.LEFT, padx=(0, 15))

        # Language selection
        ttk.Label(controls_frame, text="Language:").pack(side=tk.LEFT, padx=(0, 5))
        self.lang_var = tk.StringVar(value="en-US")
        languages = ["en-US", "es-ES", "fr-FR", "de-DE", "ja-JP", "zh-CN"]
        ttk.Combobox(
            controls_frame,
            textvariable=self.lang_var,
            values=languages,
            state="readonly",
            width=10,
        ).pack(side=tk.LEFT, padx=(0, 15))
        
        # Web search checkbox
        self.search_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            controls_frame,
            text="Search Web",
            variable=self.search_var,
            command=self.toggle_search
        ).pack(side=tk.LEFT)

        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)
        
        # Start/Stop button
        self.listen_btn = ttk.Button(
            action_frame,
            text="Start Listening",
            command=self.toggle_listening,
            width=20,
        )
        self.listen_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear and save buttons
        ttk.Button(
            action_frame, 
            text="Clear Text", 
            command=self.clear_text, 
            width=15
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Save Transcript", 
            command=self.save_text, 
            width=15
        ).pack(side=tk.RIGHT, padx=5)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var, 
            foreground="green",
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(pady=5)

        # Text area
        text_frame = ttk.LabelFrame(main_frame, text="Transcribed Text")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.text_area = scrolledtext.ScrolledText(
            text_frame, 
            wrap=tk.WORD, 
            font=("Segoe UI", 11),
            background="white",
            padx=10,
            pady=10
        )
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def toggle_search(self):
        """Toggle web search functionality"""
        self.search_web = self.search_var.get()
        if self.search_web:
            self.add_text("Web search enabled - I'll search for what you say\n")
        else:
            self.add_text("Web search disabled\n")

    def toggle_listening(self):
        """Toggle between listening and not listening states"""
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()

    def start_listening(self):
        """Start the speech recognition process"""
        self.is_listening = True
        self.listen_btn.config(text="Stop Listening")
        self.set_status("Listening...", "red")

        # Start listening thread
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()

    def stop_listening(self):
        """Stop the speech recognition process"""
        self.is_listening = False
        self.listen_btn.config(text="Start Listening")
        self.set_status("Ready", "green")

    def set_status(self, message, color):
        """Update the status message"""
        self.status_var.set(message)
        self.status_label.config(foreground=color)

    def add_text(self, text):
        """Add text to the display area"""
        self.text_area.insert(tk.END, text)
        self.text_area.see(tk.END)

    def clear_text(self):
        """Clear the text area"""
        self.text_area.delete(1.0, tk.END)

    def search_google(self, query):
        """Search the web for the given query"""
        try:
            # Format the search URL
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            # Log the search
            self.add_text(f"Searching web for: {query}\n")
            
            # Open in default browser
            webbrowser.open(search_url)
            
        except Exception as e:
            self.add_text(f"Error searching the web: {str(e)}\n")

    def listen_loop(self):
        """Main speech recognition loop"""
        engine = self.engine_var.get()
        language = self.lang_var.get()

        # Check if Sphinx is available when selected
        if engine == "sphinx":
            try:
                import pocketsphinx
            except ImportError:
                self.add_text("Sphinx engine not installed. Please run:\n")
                self.add_text("pip install pocketsphinx\n")
                self.stop_listening()
                return

        # Main recognition loop
        try:
            with self.microphone as source:
                # Adjust for ambient noise at the start
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.add_text("Listening... Speak now.\n")

                # Recognition loop
                while self.is_listening:
                    try:
                        # Listen for audio
                        audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                        
                        # Process in the main thread to avoid GUI issues
                        self.root.after(0, lambda: self.process_audio(audio, engine, language))
                        
                    except sr.WaitTimeoutError:
                        # No speech detected, continue listening
                        continue
                    except Exception as e:
                        self.add_text(f"Error: {str(e)}\n")
                        time.sleep(0.5)

        except Exception as e:
            self.add_text(f"Microphone error: {str(e)}\n")
            self.stop_listening()

    def process_audio(self, audio, engine, language):
        """Process the captured audio data"""
        self.set_status("Processing...", "orange")

        try:
            if engine == "google":
                try:
                    # Attempt to recognize with Google
                    text = self.recognizer.recognize_google(audio, language=language)
                    self.add_text(f"You said: {text}\n")
                    
                    # If web search is enabled, search for the recognized text
                    if self.search_web and text:
                        self.search_google(text)
                        
                except sr.RequestError as e:
                    self.add_text("Could not request results from Google. Check your internet connection.\n")
                except sr.UnknownValueError:
                    self.add_text("(Speech not recognized)\n")

            elif engine == "sphinx":
                try:
                    # Attempt to recognize with Sphinx
                    text = self.recognizer.recognize_sphinx(audio)
                    self.add_text(f"You said: {text}\n")
                    
                    # If web search is enabled, search for the recognized text
                    if self.search_web and text:
                        self.search_google(text)
                        
                except sr.UnknownValueError:
                    self.add_text("(Speech not recognized)\n")

        except Exception as e:
            self.add_text(f"Error: {str(e)}\n")

        # Reset status
        self.set_status(
            "Listening..." if self.is_listening else "Ready",
            "red" if self.is_listening else "green",
        )

    def save_text(self):
        """Save transcribed text to a file"""
        text = self.text_area.get(1.0, tk.END)
        if not text.strip():
            messagebox.showinfo("Info", "No text to save")
            return

        # Create a timestamped filename
        filename = f"transcription_{time.strftime('%Y%m%d_%H%M%S')}.txt"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Success", f"Saved to {os.path.abspath(filename)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")


def main():
    """Application entry point"""
    # Launch the application
    root = tk.Tk()
    app = SpeechRecognitionApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
    