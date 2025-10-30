import subprocess
import os
import wave
import re

def make_video_from_images_ffmpeg(audio_file="final_audio.wav", image_folder="images", output_file="final_output.mp4"):
    os.makedirs("temp_frames", exist_ok=True)

    
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else -1

    images = sorted(
        [img for img in os.listdir(image_folder) if img.endswith(".png")],
        key=extract_number
    )

    if not images:
        print("❌ No images found in", image_folder)
        return

    # Copy and rename images sequentially
    for i, img in enumerate(images):
        subprocess.run(["cp", os.path.join(image_folder, img), f"temp_frames/frame_{i:03d}.png"])

    # Get duration from WAV
    with wave.open(audio_file, 'rb') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        total_duration = frames / float(rate)

    per_image_duration = total_duration / len(images)

    print(f"🎧 Audio Duration: {total_duration:.2f}s")
    print(f"🖼️ Each image duration: {per_image_duration:.2f}s")

    # Step 1: Create video from images
    subprocess.run([
        "ffmpeg", "-y", "-framerate", f"1/{per_image_duration:.2f}",
        "-i", "temp_frames/frame_%03d.png",
        "-vf", "scale=1024:1024,format=yuv420p",
        "-r", "24",
        "temp_video.mp4"
    ])

    # Step 2: Add audio to video
    subprocess.run([
        "ffmpeg", "-y", "-i", "temp_video.mp4", "-i", audio_file,
        "-c:v", "copy", "-c:a", "aac", "-shortest", output_file
    ])

    # Cleanup
    subprocess.run(["rm", "-r", "temp_frames"])
    os.remove("temp_video.mp4")

    print(f"✅ Final video saved as: {output_file}")

make_video_from_images_ffmpeg()
