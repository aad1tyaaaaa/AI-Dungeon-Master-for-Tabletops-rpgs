import speech_recognition as sr
import asyncio
import logging
from typing import Optional
import tempfile
import os

from config import Config

logger = logging.getLogger(__name__)

class AudioHandler:
    """Handles speech-to-text and text-to-speech functionality"""

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts = None
        self._setup_tts_engine()
        self.audio_folder = "static/audio"
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)

    def _setup_tts_engine(self):
        """Initialize the Coqui TTS engine"""
        try:
            from TTS.api import TTS
            # Use a high-quality English TTS model
            model_name = "tts_models/en/ljspeech/tacotron2-DDC_ph"
            self.tts = TTS(model_name).to("cpu")  # Use CPU for compatibility

            logger.info("Coqui TTS engine initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Coqui TTS engine: {e}")
            logger.info("Falling back to basic TTS if available")
            self.tts = None
    
    async def text_to_speech(self, text: str) -> str:
        """Convert text to speech and save to file, return file path"""
        if not self.tts:
            logger.warning("TTS engine not available")
            return ""
        try:
            filename = f"tts_{int(asyncio.get_event_loop().time() * 1000)}.wav"
            filepath = os.path.join(self.audio_folder, filename)
            # Synthesize speech and save to file
            self.tts.tts_to_file(text=text, file_path=filepath)
            return filepath
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            return ""
    
    async def speech_to_text(self, timeout: int = 5) -> Optional[str]:
        """Convert speech to text"""
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                logger.info("Listening for speech...")
                
                audio = await asyncio.get_event_loop().run_in_executor(
                    None, 
                    lambda: self.recognizer.listen(source, timeout=timeout)
                )
                
            try:
                text = self.recognizer.recognize_google(audio)
                logger.info(f"Recognized speech: {text}")
                return text
            except sr.UnknownValueError:
                logger.warning("Could not understand audio")
                return None
            except sr.RequestError as e:
                logger.error(f"Speech recognition error: {e}")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            return None
    
    def test_audio_setup(self):
        """Test audio components"""
        if self.tts:
            self.tts.tts_to_file(text="Audio system initialized successfully", file_path=os.path.join(self.audio_folder, "test.wav"))
            return True
        return False
    
    def list_available_voices(self):
        """List all available TTS voices"""
        # Coqui TTS does not provide voice listing in this API
        return []
