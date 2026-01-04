# Gujarati Speech-to-Text Application

A Python application that converts Gujarati speech to text using OpenAI Whisper. The application records audio from your microphone and transcribes it to Gujarati text (not translated to English).

## Features

- 🎤 Records audio directly from your microphone
- 🇮🇳 Transcribes Gujarati speech to Gujarati text
- 🔒 Runs completely offline (no cloud APIs)
- 🚀 Uses OpenAI Whisper for high-quality transcription
- 💾 Saves transcriptions with timestamps

## Prerequisites

- Python 3.8 or higher
- Microphone connected to your computer
- Internet connection (only for initial package installation)

## Installation

1. **Clone or download this repository**

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install openai-whisper sounddevice soundfile numpy
   ```

3. **Note on Whisper dependencies:**
   
   Whisper requires `ffmpeg` to be installed on your system. If you encounter an error, install it:

   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use:
     ```bash
     winget install ffmpeg
     ```
     or use chocolatey:
     ```bash
     choco install ffmpeg
     ```

   - **macOS**: 
     ```bash
     brew install ffmpeg
     ```

   - **Linux (Ubuntu/Debian)**:
     ```bash
     sudo apt update && sudo apt install ffmpeg
     ```

## Usage

1. **Run the application:**

   ```bash
   python gujarati_speech_to_text.py
   ```

2. **When prompted, speak in Gujarati for 5 seconds.**

3. **The transcribed text will be displayed in the console.**

4. **The transcription will also be saved to a text file with a timestamp.**

## Configuration

You can modify the following settings in `gujarati_speech_to_text.py`:

- `RECORDING_DURATION`: How long to record (default: 5 seconds)
- `SAMPLE_RATE`: Audio sample rate (default: 16000 Hz - recommended for Whisper)
- `MODEL_NAME`: Whisper model to use:
  - `tiny`: Fastest, least accurate (almost never outputs correct Gujarati script)
  - `base`: Good balance (rarely outputs correct Gujarati script)
  - `small`: Better accuracy, but may output wrong script (Telugu/Devanagari/Latin)
  - `medium`: High accuracy, best for Gujarati script (default, recommended)
  - `large`: Best accuracy, best Gujarati script support, slowest (most reliable)
  
  **CRITICAL**: For proper Gujarati script output, use `medium` or `large` models. Smaller models (`tiny`, `base`, `small`) often output Gujarati in wrong scripts (Telugu, Devanagari, or Latin) instead of Gujarati script. This is a known limitation of Whisper with Gujarati language.

## Example Output

```
============================================================
  Gujarati Speech-to-Text Application
  Using OpenAI Whisper
============================================================

🎤 Recording audio for 5 seconds...
   Speak in Gujarati now...

✅ Recording finished!

💾 Audio saved to temporary file: C:\Users\...\temp.wav

📝 Loading Whisper model 'base'...
🔄 Transcribing audio to Gujarati text...

============================================================
  TRANSCRIPTION RESULT (Gujarati)
============================================================

હેલો, આ એક ગુજરાતી ભાષણ-થી-ટેક્સ્ટ એપ્લિકેશન છે.

============================================================

💾 Transcription saved to: transcription_20231201_143022.txt
🗑️  Temporary audio file cleaned up.
```

## How It Works

1. **Audio Recording**: Uses `sounddevice` to capture audio from your microphone at 16kHz sample rate.
2. **Audio Storage**: Saves the recorded audio to a temporary WAV file.
3. **Speech Recognition**: Uses OpenAI Whisper model with:
   - `language="gu"` (Gujarati language code)
   - `task="transcribe"` (transcribe, not translate)
4. **Output**: Displays and saves the Gujarati transcription.

## Troubleshooting

### No audio input detected
- Check that your microphone is connected and working
- Verify microphone permissions in your operating system settings
- Test your microphone with other applications

### ffmpeg not found error
- Install ffmpeg (see Installation section)
- Restart your terminal/command prompt after installing

### Model download issues
- Whisper models are downloaded automatically on first use
- Ensure you have a stable internet connection for the first run
- Models are cached after first download for offline use

### Poor transcription quality
- Speak clearly and at a moderate pace
- Reduce background noise
- Try using a larger Whisper model (small, medium, or large)
- Increase recording duration if needed

### Gujarati text appears in wrong script (Telugu/Devanagari/Latin instead of Gujarati)
This is a known limitation with Whisper models for Gujarati language. To get proper Gujarati script output:
- **Use 'medium' or 'large' model**: Change `MODEL_NAME` to `'medium'` or `'large'` in the configuration
- The `small` model may still output in wrong scripts (Telugu, Devanagari, or Latin)
- `medium` model is the recommended minimum for reliable Gujarati script output
- `large` model provides the best accuracy and most reliable Gujarati script output
- Larger models require more processing time and memory but produce correct results
- This is a known issue with Whisper's handling of Gujarati language

## License

This project uses OpenAI Whisper, which is licensed under MIT License.

## Acknowledgments

- OpenAI for the Whisper model
- sounddevice and soundfile libraries for audio handling

