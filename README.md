# AI Voice Assistant: Your Intelligent Conversational Companion

**Transform your digital interactions with your own AI Voice Assistant🎙️🤖**

This project is an advanced AI Voice Assistant that integrates Text-to-Speech (TTS) and Speech-to-Text (STT) capabilities, allowing users to communicate directly with the agent and receive vocal responses. The assistant can utilize various tools to fulfill user requests, including managing calendars, contacts, emails, and performing web searches.

## Features

- **Speech-to-Text (STT)**: Convert spoken language into written text.

- **Text-to-Speech (TTS)**: Generate vocal responses from text input.

- **Vocal Interaction**: Engage in natural conversations with the AI assistant.

- **Tool Integration**: Utilize built-in tools for calendar management, contact handling, email composition, web searching, and personal knowledge base access.

### Available Tools

- **CalendarTool**: Book events on Google Calendar with event name, date/time, and optional description.

- **AddContactTool**: Add new contacts to Google Contacts with name, phone number, and optional email address.

- **FetchContactTool**: Retrieve contact information from Google Contacts by searching with the contact's name.

- **EmailingTool**: Send emails via Gmail by providing recipient name, subject, and body content.

- **SearchWebTool**: Perform web searches to gather up-to-date information.

- **KnowledgeBaseTool**: Access the user's personal notes and saved information from your custom knowledge base (all the documents included in the `/files` folder)

## How to Run

### Prerequisites

- Python 3.9+

- Google API credentials (for Calendar, Contacts, and Gmail access)

- Tavily API key (for web search)

- Groq API key (for Llama3)

- Google Gemini API key (for using the Gemini model)

- Deepgram API key (for voice processing)

- Necessary Python libraries (listed in `requirements.txt`)

### Setup

1. **Clone the repository:**

```sh
git clone https://github.com/yourusername/AI-Voice-assistant.git
cd AI-Voice-assistant
```

2. **Create and activate a virtual environment:**

```sh
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
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

5. **Configure Google API credentials:**

Follow Google's documentation to set up credentials for Calendar, Contacts, and Gmail APIs. Save the credentials file in a secure location and update the path in the configuration file.

### Running the Application

1. **Start a conversation with the assistant:**

```sh
python main.py
```

The assistant is programmed to stop the conversation when the user says "goodbye".

## Usage Examples

- "Schedule a meeting with John for tomorrow at 2 PM."
- "Add a new contact: Jane Doe, phone number 555-1234."
- "What's Mary's email address?"
- "Send an email to Bob with the subject 'Project Update'."
- "Search the web for recent news about artificial intelligence."
- "What was the recipe I saved last week for chocolate chip cookies?"

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact

If you have any questions or suggestions, feel free to contact me at `aymenMir1001@gmail.com`.
