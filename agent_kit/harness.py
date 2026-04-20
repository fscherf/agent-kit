import json


class Harness:
    def __init__(self):
        self._tools = {}

    def add_tool(self, function):
        self._tools[function.__name__] = function

    def get_tools(self):
        return self._tools.copy()

    def handle_tool_call(self, function_name, function_arguments):
        value = ""
        exception = None

        # find tool
        if function_name not in self._tools:
            value = f"ERROR: No tool named '{function_name}' found."
            exception = KeyError(function_name)

        # run tool
        function = self._tools[function_name]

        try:
            if isinstance(function_arguments, list):
                function_return = function(*function_arguments)

            else:
                function_return = function(**function_arguments)

            value = json.dumps(function_return)

        except Exception as _exception:
            value = f"ERROR: Python exception raised while running '{function_name}': {repr(exception)}"  # NOQA
            exception = _exception

        return value, exception
