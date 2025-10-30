from kokoro import KPipeline
import soundfile as sf
import numpy as np
import os

def text_to_voice(text: str, voice: str = "am_adam", output_file: str = "final_audio.wav"):
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(text, voice=voice)

    total_duration_sec = 0
    sample_rate = 24000
    audio_segments = []
    temp_files = []

    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        duration = len(audio) / sample_rate
        total_duration_sec += duration

        temp_path = f"temp_{i}.wav"
        sf.write(temp_path, audio, sample_rate)
        temp_files.append(temp_path)

        audio_segments.append(audio)

    # Combine all segments
    full_audio = np.concatenate(audio_segments)
    sf.write(output_file, full_audio, sample_rate)

    print(f"\nSaved as: {output_file}")
    print(f"Total Audio Duration: {total_duration_sec:.2f} seconds")

    # Delete temp files
    for file in temp_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

# Load and convert
with open("./Story.txt", "r") as f:
    story = f.read()

text_to_voice(story)
