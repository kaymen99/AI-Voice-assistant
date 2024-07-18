import pyperclip
import os, time
import google.generativeai as genai
from .prompts import image_analysis_prompt
from tavily import TavilyClient

def take_screenshot():
    """
    @notice Takes a screenshot of the current screen.
    @return path The file path of the saved screenshot.
    """
    path = "./screenshot.jpg"
    # Capture the screen
    screenshot = ImageGrab.grab()
    rgb_image = screenshot.convert("RGB")
    rgb_image.save(path, quality=15)
    return path

def get_clipboard_content():
    """
    @notice Extracts the current text content from the clipboard.
    @return content The text content from the clipboard.
    """
    content = pyperclip.paste()
    print(content)
    return content

def analyze_image(prompt, path):
    """
    @notice Analyzes the image at the given path based on the provided prompt using the Gemini model.
    @param prompt The prompt to guide the image analysis.
    @param path The file path of the image to be analyzed.
    @return response The text response from the Gemini model.
    """
    # get Google API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    # configure gemini model
    genai.configure(api_key=GOOGLE_API_KEY)

    # load image
    image = Image.open(path)
    
    # call gemini-vision
    main_prompt = image_analysis_prompt.format(prompt=prompt)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([main_prompt, image], stream=True)
    response.resolve()

    return response.text

def search_web(query: str):
    """
    @notice Searches the internet for the given query.
    @param query The search query.
    @return content The combined content from the search results.
    """
    # Initialize the Tavily client for searching internet
    tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])

    content = ""
    response = tavily.search(query=query, max_results=4)
    for r in response['results']:
        content += r['content']
    return content

available_tools = {
    "take_screenshot": take_screenshot,
    "get_clipboard_content": get_clipboard_content,
    "analyze_image": analyze_image,
    "search_web": search_web
}


tools = [
    {
        "type": "function",
        "function": {
            "name": "take_screenshot",
            "description": "Takes a screenshot of the current screen and returns it as an Image object.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "capture_webcam",
            "description": "Captures an image from the webcam and returns it as a NumPy array.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_clipboard_content",
            "description": "Extracts the current text content from the clipboard.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_image",
            "description": "Analyzes a given image using a specified prompt.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to guide the image analysis."
                    },
                    "path": {
                        "type": "string",
                        "description": "The file path to the image to be analyzed."
                    }
                },
                "required": ["prompt", "path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the internet for the given query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        }
    }
]
