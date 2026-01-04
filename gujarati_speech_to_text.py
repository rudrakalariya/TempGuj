"""
Gujarati Speech-to-Text Application using OpenAI Whisper
This script records audio from the microphone and transcribes it to Gujarati text.
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
import whisper
import os
import tempfile
from datetime import datetime


def record_audio(duration=5, sample_rate=16000):
    """
    Record audio from the microphone.
    
    Args:
        duration (int): Recording duration in seconds (default: 5)
        sample_rate (int): Audio sample rate in Hz (default: 16000)
    
    Returns:
        numpy.ndarray: Recorded audio data
        int: Sample rate
    """
    print(f"\n🎤 Recording audio for {duration} seconds...")
    print("   Speak in Gujarati now...\n")
    
    # Record audio
    audio_data = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )
    
    # Wait until recording is finished
    sd.wait()
    
    print("✅ Recording finished!\n")
    
    return audio_data, sample_rate


def save_audio_temp(audio_data, sample_rate):
    """
    Save audio data to a temporary WAV file.
    
    Args:
        audio_data (numpy.ndarray): Audio data to save
        sample_rate (int): Sample rate of the audio
    
    Returns:
        str: Path to the temporary audio file
    """
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_path = temp_file.name
    temp_file.close()
    
    # Save audio to WAV file
    sf.write(temp_path, audio_data, sample_rate)
    
    return temp_path


def transcribe_audio(audio_path, model_name='base'):
    """
    Transcribe audio file to Gujarati text using Whisper.
    
    Args:
        audio_path (str): Path to the audio file
        model_name (str): Whisper model to use (tiny, base, small, medium, large)
                         Default: 'base' (good balance between speed and accuracy)
    
    Returns:
        str: Transcribed Gujarati text
    """
    print(f"📝 Loading Whisper model '{model_name}'...")
    
    # Load Whisper model
    model = whisper.load_model(model_name)
    
    print("🔄 Transcribing audio to Gujarati text...\n")
    
    # Transcribe with explicit language setting
    result = model.transcribe(
        audio_path,
        language="gu",  # Gujarati language code
        task="transcribe"  # Transcribe (not translate)
    )
    
    # Extract the transcribed text
    transcribed_text = result["text"].strip()
    
    return transcribed_text


def main():
    """
    Main function to run the Gujarati Speech-to-Text application.
    """
    print("=" * 60)
    print("  Gujarati Speech-to-Text Application")
    print("  Using OpenAI Whisper")
    print("=" * 60)
    
    # Configuration
    RECORDING_DURATION = 5  # seconds
    SAMPLE_RATE = 16000  # Hz (16kHz - preferred for Whisper)
    MODEL_NAME = 'base'  # Whisper model: tiny, base, small, medium, large
    
    audio_path = None
    
    try:
        # Step 1: Record audio from microphone
        audio_data, sample_rate = record_audio(
            duration=RECORDING_DURATION,
            sample_rate=SAMPLE_RATE
        )
        
        # Step 2: Save audio to temporary WAV file
        audio_path = save_audio_temp(audio_data, sample_rate)
        print(f"💾 Audio saved to temporary file: {audio_path}\n")
        
        # Step 3: Transcribe audio to Gujarati text
        transcribed_text = transcribe_audio(audio_path, model_name=MODEL_NAME)
        
        # Step 4: Display results
        print("=" * 60)
        print("  TRANSCRIPTION RESULT (Gujarati)")
        print("=" * 60)
        print(f"\n{transcribed_text}\n")
        print("=" * 60)
        
        # Optional: Save transcription to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"transcription_{timestamp}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcribed_text)
        print(f"\n💾 Transcription saved to: {output_file}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Recording interrupted by user.")
    except Exception as e:
        print(f"\n❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up temporary audio file
        if audio_path and os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"\n🗑️  Temporary audio file cleaned up.")


if __name__ == "__main__":
    main()

