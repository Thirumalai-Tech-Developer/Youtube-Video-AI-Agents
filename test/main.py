import requests
import numpy as np
from PIL import Image
import os

IMAGE_VIDEO = os.getenv("IMAGE_VIDEO")

img = Image.open("pony_result.png").convert("RGB").resize((1024, 1024))
img_np = np.array(img, dtype=np.uint8)

response = requests.post(
    f"{IMAGE_VIDEO}/i2v",
    json={"image": img_np.tolist()}  # Send the image as nested list
)

if response.status_code == 200:
    print("recieved")
    with open("video.mp4", "wb") as f:
        f.write(response.content)
    print("🎉 Saved as video.mp4")
else:
    print("❌ Error:", response.status_code, response.text)
