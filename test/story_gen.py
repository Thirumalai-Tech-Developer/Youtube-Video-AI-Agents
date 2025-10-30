import requests

API_KEY = "AIzaSyANy3IajOCVcoV5Gn-0RQ-K5DpqBn2SSeg"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent?key={API_KEY}"

def build_clean_voiceover_prompt(keywords):
    return f"""
Write a short, dramatic YouTube narration (75–150 words) using the following keywords:

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


topic = "King, Queen, God, Alien"
prompt = build_clean_voiceover_prompt(topic)

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

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        with open("Story.txt", "w") as f:
            res = result.get('candidates')[0]['content']['parts'][0]['text']
            f.write(res)
            return res
        
    else:
        print("Error:", response.status_code, response.text)

story(prompt)



