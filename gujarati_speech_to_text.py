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


def transcribe_audio(audio_path, model_name='medium'):
    """
    Transcribe audio file to Gujarati text using Whisper.
    
    Args:
        audio_path (str): Path to the audio file
        model_name (str): Whisper model to use (tiny, base, small, medium, large)
                         Default: 'medium' (recommended for Gujarati script output)
    
    Returns:
        tuple: (transcribed_text, language_detected)
    """
    print(f"📝 Loading Whisper model '{model_name}'...")
    print("   (Note: 'medium' or 'large' models are recommended for proper Gujarati script output)\n")
    
    # Load Whisper model
    model = whisper.load_model(model_name)
    
    print("🔄 Transcribing audio to Gujarati text...\n")
    
    # Transcribe with explicit language setting
    result = model.transcribe(
        audio_path,
        language="gu",  # Gujarati language code
        task="transcribe",  # Transcribe (not translate)
        fp16=False,  # Use FP32 for CPU (avoids warning)
        verbose=False  # Reduce verbose output
    )
    
    # Extract the transcribed text and detected language
    transcribed_text = result["text"].strip()
    detected_language = result.get("language", "unknown")
    
    # Show language detection info
    print(f"📊 Detected language: {detected_language}")
    
    return transcribed_text, detected_language


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
    # IMPORTANT: For proper Gujarati script output, 'medium' or 'large' models are recommended
    # 'small' model may still output in wrong script (Telugu/Latin/Devanagari)
    # 'tiny' and 'base' models almost always fail to produce Gujarati script
    MODEL_NAME = 'medium'  # Whisper model: tiny, base, small, medium, large (recommended: medium or large)
    
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
        transcribed_text, detected_lang = transcribe_audio(audio_path, model_name=MODEL_NAME)
        
        # Step 4: Display results
        print("\n" + "=" * 60)
        print("  TRANSCRIPTION RESULT")
        print("=" * 60)
        print(f"Detected Language: {detected_lang}")
        print(f"Output Text:\n")
        print(transcribed_text)
        print("\n" + "=" * 60)
        
        # Check if output is in the correct script (Gujarati Unicode range: U+0A80 to U+0AFF)
        has_gujarati_script = any('\u0a80' <= char <= '\u0aff' for char in transcribed_text)
        
        # Detect other common scripts that might appear incorrectly
        has_telugu_script = any('\u0c00' <= char <= '\u0c7f' for char in transcribed_text)
        has_devanagari_script = any('\u0900' <= char <= '\u097f' for char in transcribed_text)
        has_tamil_script = any('\u0b80' <= char <= '\u0bff' for char in transcribed_text)
        
        if detected_lang == "gu" and not has_gujarati_script:
            print("\n⚠️  WARNING: Output is NOT in Gujarati script!")
            if has_telugu_script:
                print("   Detected: Telugu script instead of Gujarati script.")
            elif has_devanagari_script:
                print("   Detected: Devanagari script instead of Gujarati script.")
            elif has_tamil_script:
                print("   Detected: Tamil script instead of Gujarati script.")
            else:
                print("   Detected: Latin/Romanized script instead of Gujarati script.")
            
            print("\n   SOLUTIONS:")
            print("   1. Try a LARGER model: Change MODEL_NAME to 'medium' or 'large'")
            print("      (The 'small' model may still produce incorrect script for Gujarati)")
            print("   2. Ensure you're speaking clearly in Gujarati")
            print("   3. This is a known Whisper limitation with Gujarati language")
            print("   4. Consider using Whisper 'medium' or 'large' model for better results\n")
        
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

