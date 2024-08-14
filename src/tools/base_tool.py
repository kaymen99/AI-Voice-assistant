from abc import ABC, abstractmethod
from instructor import OpenAISchema


# Define the BaseTool abstract class
class BaseTool(ABC, OpenAISchema):
    @abstractmethod
    def run(self):
        pass
