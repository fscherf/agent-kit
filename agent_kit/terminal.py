def color(text, color_name):
    color_code = {
        "grey": "\033[90m",
        "bold-red": "\033[1;91m",
        "bold-green": "\033[1;32m",
    }[color_name]

    return f"{color_code}{text}\033[0m"
