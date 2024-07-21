# AI-Voice-Assistant

This project is an advanced AI Voice Assistant that integrates both Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities, allowing users to communicate directly with the agent and receive vocal responses. The agent can utilize various tools to fulfill user requests and can be extended with additional tools as needed.

## Features

- **Speech-to-Text (STT)**: Convert spoken language into written text.
- **Text-to-Speech (TTS)**: Generate vocal responses from text input.
- **Vocal Interaction**: Engage in natural conversations with the AI assistant.
- **Tool Integration**: Utilize built-in tools such as web search, clipboard extraction, screenshot capturing, and image analysis. Additional tools can be integrated as needed.

### Available Tools

- **search_web**: Performs web searches with Tavily to collect the most up-to-date information.
- **extract_clipboard**: Extracts and utilizes any text present in the user's clipboard.
- **take_screenshot**: Captures the current screen as an image upon user request.
- **analyze_image**: Use the Gemini vision model to analyze given images or any visual-related queries by providing a specific prompt and path of the image.

## How to Run

### Prerequisites

- Python 3.9+
- Tavily API key
- Groq API key (for Llama3)
- Google Gemini API key (for using the Gemini model)
- Deepgram API key (for voice processing)
- Necessary Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://github.com/kaymen99/AI-Voice-assistant.git
   cd AI-Voice-assistant
   ```

2. **Create and activate a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root directory of the project and add your API keys:

   ```env
   GOOGLE_API_KEY=your_google_api_key
   DEEPGRAM_API_KEY=your_deepgram_api_key
   TAVILY_API_KEY=your_tavily_api_key
   GEMINI_API_KEY=your_gemini_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

### Running the Application

1. **Start a conversation with the assistant with:**

   ```sh
   python main.py
   ```

   The assistant is programmed to stop the conversation whenever the word "goodbye" is said by the user.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

If you have any questions or suggestions, feel free to contact me at `aymenMir10001@gmail.com`.