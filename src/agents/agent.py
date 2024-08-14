from colorama import Fore, init
from litellm import completion

# Initialize colorama for colored terminal output
init(autoreset=True)


class Agent:
    def __init__(self, name, model, tools=None, system_prompt=""):
        self.name = name
        self.model = model
        self.messages = []
        self.tools = tools if tools is not None else []
        self.tools_schemas = self.get_openai_tools_schema() if self.tools else None
        self.system_prompt = system_prompt
        if self.system_prompt and not self.messages:
            self.handle_messages_history("system", self.system_prompt)

    def invoke(self, message):
        print(Fore.GREEN + f"\nCalling Agent: {self.name}")
        self.handle_messages_history("user", message)
        result = self.execute()
        return result

    def execute(self):
        response_message = self.call_llm()
        response_content = response_message.content
        tool_calls = response_message.tool_calls
        if tool_calls:
            try:
                response_content = self.run_tools(tool_calls)
            except Exception as e:
                print(Fore.RED + f"\nError: {e}\n")
        return response_content

    def run_tools(self, tool_calls):
        for tool_call in tool_calls:
            self.execute_tool(tool_call)
        response_content = self.execute()
        return response_content

    def execute_tool(self, tool_call):
        function_name = tool_call.function.name
        func = next(
            iter([func for func in self.tools if func.__name__ == function_name])
        )

        if not func:
            return f"Error: Function {function_name} not found. Available functions: {[func.__name__ for func in self.tools]}"

        try:
            print(Fore.GREEN + f"\nCalling Tool: {function_name}")
            print(Fore.GREEN + f"Arguments: {tool_call.function.arguments}\n")
            func = func(**eval(tool_call.function.arguments))
            output = func.run()

            tool_message = {"name": function_name, "tool_call_id": tool_call.id}
            self.handle_messages_history("tool", output, tool_output=tool_message)

            return output
        except Exception as e:
            print("Error: ", str(e))
            return "Error: " + str(e)

    def call_llm(self):
        response = completion(
            model=self.model,
            messages=self.messages,
            tools=self.tools_schemas,
            temperature=0.1,
        )
        message = response.choices[0].message
        if message.tool_calls is None:
            message.tool_calls = []
        if message.function_call is None:
            message.function_call = {}
        self.handle_messages_history(
            "assistant", message.content, tool_calls=message.tool_calls
        )
        return message

    def get_openai_tools_schema(self):
        return [
            {"type": "function", "function": tool.openai_schema} for tool in self.tools
        ]

    def reset(self):
        self.memory.clear_messages()
        self.messages = []
        if self.system_prompt:
            self.handle_messages_history("system", self.system_prompt)

    def handle_messages_history(self, role, content, tool_calls=None, tool_output=None):
        message = {"role": role, "content": content}
        if tool_calls:
            message["tool_calls"] = self.parse_tool_calls(tool_calls)
        if tool_output:
            message["name"] = tool_output["name"]
            message["tool_call_id"] = tool_output["tool_call_id"]
        # save short-term memory
        self.messages.append(message)

    def parse_tool_calls(self, calls):
        parsed_calls = []
        for call in calls:
            parsed_call = {
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                },
                "id": call.id,
                "type": call.type,
            }
            parsed_calls.append(parsed_call)
        return parsed_calls
