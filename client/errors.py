class MyAppError(Exception):
    ...

class MissingArgument(MyAppError):
    def __init__(self, argument_name: str, mode: str | None = None):
        message = argument_name + " is required"
        if mode:
            message += " in mode " + mode
        super().__init__(message)
