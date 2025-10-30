import requests
import os
import dotenv

dotenv.load_dotenv()  # 👈 Load .env file

TEXT = os.getenv("TEXT")

prompt = """
You are a professional YouTube scriptwriter.  

Write an engaging, short script (150–200 words) for a video using the following keywords:

**Keywords:** [INSERT TO TOPIC AS YOUR WISH]

The script should:
- Start with a powerful **hook** that grabs attention.
- Present the story in **3 short scenes or paragraphs** (as if visualized in a video).
- End with an **intriguing conclusion or call to action**.
- Use a storytelling tone that’s informative, creative, and easy to understand.

Keep the language simple and dramatic. Don't use headings or scene labels.

Begin:
"""


response = requests.post(
    f"{TEXT}/story",
    json={"prompt": prompt}
)

if response.status_code == 200:
    print("✅ Received Text")
    story_text = response.json().get("story")
    with open("Story.txt", "w") as f:
        f.write(story_text)
    print("🎉 Saved as Story.txt")
    print(response.content)
else:
    print("❌ Error:", response.status_code, response.text)