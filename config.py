import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the AI Dungeon Master"""
    
    # Gemini Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")
    
    # Audio Configuration
    SPEECH_RATE = 200
    SPEECH_VOLUME = 0.9
    VOICE_ID = None  # None for default voice
    
    # Game Configuration
    MAX_STORY_LENGTH = 1000
    NPC_MEMORY_LENGTH = 10
    WORLD_BUILDING_DEPTH = 3
    
    # Audio Files
    TEMP_AUDIO_FILE = "temp_audio.wav"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required. Please set it in your .env file.")
