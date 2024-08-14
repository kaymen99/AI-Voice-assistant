from .speech_to_text import get_transcript
from .text_to_speech import TTS


class ConversationManager:
    def __init__(self, assistant):
        self.transcription_response = ""
        self.assistant = assistant

    async def main(self):
        def handle_full_sentence(full_sentence):
            self.transcription_response = full_sentence

        # Loop indefinitely until "goodbye" is said
        while True:
            await get_transcript(handle_full_sentence)
            
            # Check for "goodbye" to exit the loop
            if "goodbye" in self.transcription_response.lower():
                break
            
            llm_response = self.assistant.invoke(self.transcription_response)
            print(f"AI: {llm_response}")

            tts = TTS()
            tts.speak(llm_response)

            # Reset transcription_response for the next loop iteration
            self.transcription_response = ""