import requests
import os
from kokoro import KPipeline
import soundfile as sf
import dotenv
import numpy as np
import soundfile as sf
from PIL import Image
from kokoro import KPipeline


dotenv.load_dotenv()

IMAGE_VIDEO = "https://capitol-suse-studying-periodically.trycloudflare.com"
TEXT_IMAGE = "https://zones-controversy-cathedral-percent.trycloudflare.com"
TEXT_KEY = "AIzaSyANy3IajOCVcoV5Gn-0RQ-K5DpqBn2SSeg"
TEXT_GEN = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent?key={TEXT_KEY}"


def build_story_prompt(keywords):
    return f"""
Write a short, dramatic YouTube narration (75–100 words) using the following keywords:

**Keywords:** {keywords}

Instructions:
- Use a cinematic, emotionally engaging tone suitable for voice narration.
- Do NOT include scene labels, timestamps, or formatting like (Scene 1), (Music), or (Voiceover).
- Speak directly to the viewer in a natural, immersive way.
- Begin with a powerful hook.
- Develop the story in 3 natural flowing parts (but don't label them).
- End with a mysterious or thought-provoking question or a strong call to action.
- Keep the language simple but dramatic.
- Output only the narration script, no headings or metadata.

Begin:
"""

def build_image_prompt(story: str, num_prompts: int = 15):
    import math

    words = story.strip().split()
    total_words = len(words)

    # Words per chunk (rounded to nearest whole number)
    words_per_chunk = max(1, round(total_words / num_prompts))

    # Split into chunks
    chunks = []
    for i in range(0, total_words, words_per_chunk):
        chunk = " ".join(words[i:i + words_per_chunk])
        chunks.append(chunk)

    # Ensure only num_prompts number of prompts
    if len(chunks) > num_prompts:
        chunks = chunks[:num_prompts]

    # Format prompt instructions
    prompt_blocks = []
    for i, chunk in enumerate(chunks):
        prompt_blocks.append(f"{i+1}. Prompt : Describe this scene visually - \"{chunk.strip()}\"")

    prompt_text = "\n".join(prompt_blocks)

    full_prompt = f"""
                    You are an expert image prompt generator for AI models like Stable Diffusion.

                    Instructions:
                    - Use the description inside quotes for each prompt as the scene content.
                    - Focus on visual storytelling — include setting, characters, atmosphere, emotion, lighting.
                    - Each prompt should be a vivid, concise description (max 10–20 words).
                    - Do NOT include any intro or extra lines.
                    - Format as:
                    1. Prompt : ...
                    2. Prompt : ...
                    ...
                    {num_prompts}. Prompt : ...

                    Scene Descriptions:
                    {prompt_text}
                    """
    return full_prompt.strip()



def process_image_prompts(prompt_input, output_format="list", file_path=None):
    """
    Processes a string or list of image prompts into structured formats.

    Parameters:
        prompt_input (str or list): Multi-line string or list of prompts.
        output_format (str): 'list', 'json', or 'plain'. Default is 'list'.
        file_path (str): Optional. If provided, saves output to file.

    Returns:
        Processed output in specified format.
    """

    import json
    import re

    # Handle input: list or multiline string
    if isinstance(prompt_input, str):
        lines = prompt_input.strip().split('\n')
    else:
        lines = prompt_input

    # Extract numbered prompts cleanly
    prompts = []
    for line in lines:
        match = re.search(r'^\d+\.\s*Prompt\s*:?\s*(.+)', line.strip(), re.IGNORECASE)
        if match:
            prompts.append(match.group(1).strip())

    # Format options
    if output_format == "list":
        result = prompts
    elif output_format == "json":
        result = [{"id": i+1, "prompt": p} for i, p in enumerate(prompts)]
    elif output_format == "plain":
        result = "\n".join(prompts)
    else:
        raise ValueError("Unsupported format. Use 'list', 'json', or 'plain'.")

    # Save to file if requested
    if file_path:
        with open(file_path, 'w') as f:
            if output_format == "json":
                json.dump(result, f, indent=2)
            else:
                f.write(result if isinstance(result, str) else "\n".join(result))

    return result

def story(story_prompt):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": story_prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(TEXT_GEN, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        with open("Story.txt", "w") as f:
            res = result.get('candidates')[0]['content']['parts'][0]['text']
            f.write(res)
            return res
        
    else:
        print("Error:", response.status_code, response.text)

def images(image_prompt):
    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": image_prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(TEXT_GEN, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        with open("image.txt", "w") as f:
            res = result.get('candidates')[0]['content']['parts'][0]['text']
            f.write(res)
            return res
        
    else:
        print("Error:", response.status_code, response.text)

def text_to_voice(text: str, voice: str = "am_adam", output_file: str = "final_audio.wav"):
    pipeline = KPipeline(lang_code='a')
    generator = pipeline(text, voice=voice)

    total_duration_sec = 0
    sample_rate = 24000
    audio_segments = []
    temp_files = []

    for i, (gs, ps, audio) in enumerate(generator):
        # print(i, gs, ps)
        duration = len(audio) / sample_rate
        total_duration_sec += duration

        temp_path = f"temp_{i}.wav"
        sf.write(temp_path, audio, sample_rate)
        temp_files.append(temp_path)

        audio_segments.append(audio)

    # Combine all segments
    full_audio = np.concatenate(audio_segments)
    sf.write(output_file, full_audio, sample_rate)

    # print(f"\nSaved as: {output_file}")
    # print(f"Total Audio Duration: {total_duration_sec:.2f} seconds")

    # Delete temp files
    for file in temp_files:
        try:
            os.remove(file)
        except Exception as e:
            print(f"Failed to delete {file}: {e}")

    return total_duration_sec

story_prompt_keywords = "Ironman vs Spiderman atlast Ironman has to be win"
story_prompt = build_story_prompt(story_prompt_keywords)

sto = story(story_prompt)

duration = text_to_voice(sto)

num_prompts = round(round(duration) / 3)

image_prompt = build_image_prompt(sto, num_prompts)

image = images(image_prompt)

image_prompt_list = process_image_prompts(image)

for i, prompt in enumerate(image_prompt_list):
    try:
        response = requests.post(f"{TEXT_IMAGE}/t2i", json={"prompt": prompt})
        if response.status_code == 200:
            with open(f"images/out_{i+1}.png", "wb") as f:
                f.write(response.content)
            print(f"🎉 Saved as out_{i+1}.png")
        else:
            print(f"❌ Error generating image {i+1}: {response.status_code}\n{response.text}")
    except Exception as e:
        print(f"❌ Exception while generating image {i+1}: {e}")

image_name = os.listdir("./images")

# for i in range(len(image_name)):
#     img = Image.open(f"./images/{image_name[i]}").convert("RGB").resize((1024, 1024))
#     img_np = np.array(img, dtype=np.uint8)

#     response = requests.post(
#         f"{IMAGE_VIDEO}/i2v",
#         json={"image": img_np.tolist()}  # Send the image as nested list
#     )

#     if response.status_code == 200:
#         print("recieved")
#         with open(f"videos/video_{i}.mp4", "wb") as f:
#             f.write(response.content)
#         print(f"🎉 Saved as video_{i}.mp4")
#     else:
#         print("❌ Error:", response.status_code, response.text)

# import os
# import subprocess

# def final_video_ffmpeg():
#     # Step 1: Create videos.txt with paths of video clips
#     video_files = sorted([f for f in os.listdir("videos") if f.endswith(".mp4")])
#     with open("videos.txt", "w") as f:
#         for vf in video_files:
#             f.write(f"file 'videos/{vf}'\n")

#     # Step 2: Concatenate videos (make sure they have same codec, resolution, etc.)
#     subprocess.run([
#         "ffmpeg", "-f", "concat", "-safe", "0", "-i", "videos.txt", "-c", "copy", "temp_output.mp4"
#     ])

#     # Step 3: Merge audio
#     subprocess.run([
#         "ffmpeg", "-i", "temp_output.mp4", "-i", "final_audio.mp3", "-c:v", "copy", "-c:a", "aac", "-shortest", "final_output.mp4"
#     ])

#     # Cleanup
#     os.remove("videos.txt")
#     os.remove("temp_output.mp4")

# final_video_ffmpeg()

import subprocess
import os
import wave

def make_video_from_images_ffmpeg(audio_file="final_audio.wav", image_folder="images", output_file="final_output.mp4"):
    os.makedirs("temp_frames", exist_ok=True)

    images = sorted([img for img in os.listdir(image_folder) if img.endswith(".png")])
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
