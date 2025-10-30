import requests

API_KEY = "AIzaSyANy3IajOCVcoV5Gn-0RQ-K5DpqBn2SSeg"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent?key={API_KEY}"

# Read the story from file
with open("Story.txt", 'r') as f:
    story = f.read()

# Estimate number of image prompts based on story length
num_prompts = int((len(story.split()) * 0.5) // 7)

prompt = f"""
You are an expert AI image prompt generator for text-to-image models like Stable Diffusion.

Your task is to read the story below and extract exactly {num_prompts} visual moments as short, vivid prompts for image generation.

Instructions:
- Each prompt should describe one specific scene or visual from the story.
- Focus on composition, objects, atmosphere, lighting, and emotional tone.
- Keep each prompt concise (max 8–10 words), but rich in visual meaning.
- Do NOT include any intro, explanation, or numbering beyond the list format.
- Do NOT mention that this is based on a story.
- Just return the prompt list directly in the format:
1. Prompt : ...
2. Prompt : ...
...
{num_prompts}. Prompt : ...

Story:
{story}
"""


headers = {
    "Content-Type": "application/json"
}

data = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ]
}

# Send request to Gemini API
response = requests.post(url, headers=headers, json=data)

# Save result to Story.txt if successful
if response.status_code == 200:
    result = response.json()
    image_prompts = result['candidates'][0]['content']['parts'][0]['text']
    with open("image.txt", "w") as f:
        f.write(image_prompts)
    print("✅ Image prompts saved to Story.txt")
else:
    print("❌ Error:", response.status_code, response.text)
