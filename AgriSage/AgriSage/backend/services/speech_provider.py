from typing import Dict, Any
from abc import ABC, abstractmethod


class SpeechProviderInterface(ABC):
    @abstractmethod
    async def synthesize_speech(self, text: str, language: str = "ml") -> Dict[str, Any]:
        """Synthesize vernacular audio payload from advisory text."""
        pass


class SpeechProvider(SpeechProviderInterface):
    """Vernacular Text-to-Speech (TTS) Provider for Malayalam and English audio narration."""

    async def synthesize_speech(self, text: str, language: str = "ml") -> Dict[str, Any]:
        return {
            "text": text,
            "language": language,
            "format": None,
            "sample_rate_hz": None,
            "audio_base64": None,
            "duration_seconds": None,
            "available": False,
            "warning": "Text-to-speech provider is not configured; no audio was generated.",
        }
