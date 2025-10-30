import requests
import os
import dotenv

dotenv.load_dotenv()  # 👈 Load .env file

TEXT = os.getenv("TEXT")

with open("Story.txt", 'r') as f:
    story = f.read()

lis = story.split()

lis = int((len(lis) * 0.5) // 7)


prompt = f"""
You are a professional AI image prompt engineer.  
Read the story context below and generate visual scene prompts.

Each prompt should:
- Describe one specific scene or visual moment from the story
- Include details like setting, characters, action, lighting, mood
- Be in the style of AI image generation prompts (like Stable Diffusion)
- Be concise and clear (under 5-8 words per prompt)

---

Story Context:
{story}
---

Now, generate image prompts based on this story, labeled clearly as:
1. Prompt 1: ...
2. Prompt 2: ...
...
{lis}. Prompt {lis}: ...
"""

# print(prompt)
response = requests.post(
    f"{TEXT}/story",
    json={"prompt": prompt}
)

if response.status_code == 200:
    print("✅ Received Text")
    story_text = response.json().get("story")
    with open("image.txt", "w") as f:
        f.write(story_text)
    print("🎉 Saved as image.txt")
    print(response.content)
else:
    print("❌ Error:", response.status_code, response.text)