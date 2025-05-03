# Speech Recognition App with Web Search

A simple desktop application that performs real-time speech recognition and can automatically search the web for your queries.

## Features

- **Real-time Speech Recognition:** Convert your voice to text as you speak
- **Multiple Recognition Engines:** Support for Google (online) and Sphinx (offline) engines
- **Multiple Languages:** Support for various languages including English, Spanish, French, German, Japanese, and Chinese
- **Web Search Integration:** Optionally search the web for what you say
- **Save Transcripts:** Save your transcribed speech to a text file

## Screenshots

![Speech Recognition App](screenshots/app_screenshot.png)

## Requirements

- Python 3.8 or higher
- SpeechRecognition library
- PyAudio
- tkinter (included with most Python installations)
- PocketSphinx (optional, for offline recognition)

## Installation

1. Clone this repository or download the source code:
```
git clone https://github.com/yourusername/speech-recognition-app.git
cd speech-recognition-app
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. For offline recognition with Sphinx (optional):
```
pip install pocketsphinx
```

## Usage

1. Run the application:
```
python main.py
```

2. Click "Start Listening" and speak clearly into your microphone
3. Your speech will be transcribed in the text area
4. To search the web for what you say, check the "Search Web" checkbox
5. Use the "Save Transcript" button to save your session

## Troubleshooting

**Microphone not working:**
- Make sure your microphone is properly connected and configured as the default recording device
- If using Windows, try selecting "Microphone Array" in your sound settings
- If PyAudio fails to install, try:
  ```
  pip install pipwin
  pipwin install pyaudio
  ```

**Recognition accuracy issues:**
- Speak clearly and at a normal pace
- Reduce background noise
- Position the microphone closer to your mouth

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SpeechRecognition library for providing the speech recognition capabilities
- Google and CMU Sphinx for their speech recognition engines