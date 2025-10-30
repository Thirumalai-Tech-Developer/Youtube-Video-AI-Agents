# Youtube Video AI Agents


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