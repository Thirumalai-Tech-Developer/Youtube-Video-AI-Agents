# Youtube Video AI Agents

## Overview
This repository contains a Python script for converting images to videos using an AI service.

## Features
- Image to video conversion
- Support for 1024x1024 RGB images
- REST API integration
- Simple file handling

## Installation
```bash
pip install requests
pip install numpy
pip install Pillow
```

## Usage
```python
# Set the IMAGE_VIDEO environment variable with your service URL
# Place your input image as "pony_result.png" in the same directory

import requests
import numpy as np
from PIL import Image

# The script will:
# 1. Load and resize the image to 1024x1024
# 2. Convert it to video using the AI service
# 3. Save the result as "video.mp4"
```

## Environment Variables
- `IMAGE_VIDEO`: URL of the image-to-video conversion service

## Contributing
## Main Components

### Story Generation
- Uses Gemma 3 27b AI model for generating cinematic YouTube narration
- Takes keywords as input and produces emotionally engaging stories
- Story length optimized for YouTube format (75-100 words)

### Image Generation
- Converts story into multiple image prompts
- Each prompt represents a key story segment
- Uses AI image generation to create visual scenes
- Outputs 1024x1024 RGB images

### Voice Generation 
- Converts story text to natural-sounding speech
- Uses Kokoro TTS pipeline
- Outputs high-quality WAV audio (24kHz)
- Handles timing and segmentation

### Video Creation
- Combines generated images into video frames
- Synchronizes with generated audio
- Uses FFmpeg for final video compilation
- Creates smooth transitions between scenes

### Required APIs
- TEXT_GEN: Gemma text generation API
- TEXT_IMAGE: Image generation endpoint 
- IMAGE_VIDEO: Video processing service

## Dependencies
```bash
pip install requests soundfile python-dotenv numpy Pillow kokoro
```

## Environment Setup
Create .env file with:
```
TEXT_KEY=your_gemma_api_key
```

## License
MIT - See LICENSE file for details

## Contact
Create an issue in this repository for questions