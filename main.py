import time, asyncio
from dotenv import load_dotenv
from colorama import Fore, Style, init
from utils.agent import Agent
from utils.prompts import assistant_prompt
from utils.tools import tools, available_tools
from utils.speech_to_text import get_transcript
from utils.text_to_speech import TTS

load_dotenv()

class ConversationManager:
    def __init__(model, self):
        self.transcription_response = ""
        self.assistant = Agent(
                            name="AI Assistant",
                            model=model,
                            tools=tools,
                            available_tools=available_tools,
                            system_prompt=assistant_prompt
                        )

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

if __name__ == "__main__":
    MODEL = "groq/llama3-70b-8192"
    manager = ConversationManager(MODEL)
    asyncio.run(manager.main())