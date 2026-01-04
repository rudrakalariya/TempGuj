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
  - `medium`: High accuracy, good balance between speed and accuracy (default, recommended)
  - `large`: Best accuracy, most reliable for Gujarati script, but slower
  
  **CRITICAL**: For reliable Gujarati script output, use the `medium` or `large` model. The code uses an `initial_prompt` with Gujarati text to guide the model. The `medium` model is a good balance between speed and accuracy. If you still get wrong scripts, try the `large` model which is most reliable. Smaller models (`tiny`, `base`, `small`) often output in wrong scripts (Telugu, Devanagari, or Latin) instead of Gujarati script. This is a known limitation of Whisper with Gujarati language.

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
This is a known limitation with Whisper models for Gujarati language. Even though we explicitly specify `language="gu"` and use an `initial_prompt` in Gujarati script, smaller models may still output in wrong scripts. Solutions:
- **Try 'large' model**: If `medium` model fails, change `MODEL_NAME` to `'large'` (most reliable)
- The code includes an `initial_prompt` with Gujarati text to guide the model
- Even with `language="gu"` explicitly set, `small` and sometimes `medium` models may output wrong scripts
- `medium` model is a good balance; `large` model is most reliable but slower
- This is a fundamental limitation of Whisper's training with Gujarati language data
- The `large` model requires more processing time and memory but produces correct results

## License

This project uses OpenAI Whisper, which is licensed under MIT License.

## Acknowledgments

- OpenAI for the Whisper model
- sounddevice and soundfile libraries for audio handling

