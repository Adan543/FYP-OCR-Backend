from gtts import gTTS
import os
import base64

def text_to_speech(text):
    """Convert text to speech and return Base64 encoded audio."""
    try:
        tts = gTTS(text=text, lang="ur")
        file_path = "output.mp3"
        tts.save(file_path)

        with open(file_path, "rb") as audio_file:
            base64_audio = base64.b64encode(audio_file.read()).decode("utf-8")

        os.remove(file_path)
        return base64_audio

    except Exception as e:
        return str(e)
