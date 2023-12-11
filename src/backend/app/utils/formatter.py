def format_exception(exception: Exception) -> str:
    return f"An exception occurred. Exception type: {type(exception).__name__}. Arguments: {','.join(map(str, exception.args))}"