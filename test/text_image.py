import requests
import os
import dotenv

dotenv.load_dotenv()  # 👈 Load .env file

TEXT_IMAGE = os.getenv("TEXT_IMAGE")

prompt = "fantacy king with fantacy beast"

response = requests.post(
    f"{TEXT_IMAGE}/t2i",
    json={"prompt": prompt}
)

if response.status_code == 200:
    print("✅ Received image")
    with open("image.png", "wb") as f:
        f.write(response.content)
    print("🎉 Saved as image.png")
else:
    print("❌ Error:", response.status_code, response.text)