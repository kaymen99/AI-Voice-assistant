import asyncio
from dotenv import load_dotenv
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone
)

# Load environment variables from a .env file
load_dotenv()

class TranscriptCollector:
    def __init__(self):
        self.reset()

    def reset(self):
        # Initialize or reset the transcript parts list
        self.transcript_parts = []

    def add_part(self, part):
        # Add a part of the transcript to the list
        self.transcript_parts.append(part)

    def get_full_transcript(self):
        # Join all parts of the transcript into a single string
        return ' '.join(self.transcript_parts)

# Create an instance of TranscriptCollector to manage transcript parts
transcript_collector = TranscriptCollector()

async def get_transcript(callback):
    # Event to signal transcription completion
    transcription_complete = asyncio.Event()

    try:
        # Example of setting up a Deepgram client config
        config = DeepgramClientOptions(options={"keepalive": "true"})
        deepgram: DeepgramClient = DeepgramClient("", config)

        # Initialize a connection to Deepgram's asynchronous websocket API
        dg_connection = deepgram.listen.asyncwebsocket.v("1")
        print("Listening...")

        async def on_message(self, result, **kwargs):
            # Extract the transcript from the result
            sentence = result.channel.alternatives[0].transcript
            
            if not result.speech_final:
                # Add interim results to the transcript collector
                transcript_collector.add_part(sentence)
            else:
                # Add the final part of the current sentence to the transcript collector
                transcript_collector.add_part(sentence)
                # Get the full sentence from the transcript collector
                full_sentence = transcript_collector.get_full_transcript()
                # Check if the full sentence is not empty before printing
                if len(full_sentence.strip()) > 0:
                    full_sentence = full_sentence.strip()
                    print(f"Human: {full_sentence}")
                    # Call the callback with the full sentence
                    callback(full_sentence)
                    # Reset the transcript collector for the next sentence
                    transcript_collector.reset()
                    # Signal to stop transcription and exit
                    transcription_complete.set()

        # Set up the event listener for transcription events
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        # Define the options for live transcription
        options = LiveOptions(
            model="nova-2",
            punctuate=True,
            language="en-US",
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=300,
            smart_format=True,
        )

        # Start the connection with the specified options
        await dg_connection.start(options)

        # Open a microphone stream on the default input device
        microphone = Microphone(dg_connection.send)
        microphone.start()

        # Wait for the transcription to complete
        await transcription_complete.wait()

        # Wait for the microphone to close
        microphone.finish()

        # Indicate that we've finished
        await dg_connection.finish()

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

# Global variable to store the transcription response
transcription_response = ""

def handle_full_sentence(full_sentence):
    global transcription_response
    transcription_response = full_sentence

if __name__ == "__main__":
    # Run the get_transcript function and pass handle_full_sentence as the callback
    asyncio.run(get_transcript(handle_full_sentence))