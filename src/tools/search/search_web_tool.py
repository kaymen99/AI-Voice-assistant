import os
from pydantic import Field
from ..base_tool import BaseTool
from tavily import TavilyClient

class SearchWebTool(BaseTool):
    """
    A tool that searches the internet and get up to date information for a given query
    """
    query: str = Field(description='Search query string')

    def search_web(self, query: str):
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
    
    def run(self):
        return self.search_web(self.query)

