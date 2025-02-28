def sanitize_for_code(message):
    return {
        "role": message["role"],
        "content": message["content"].translate(str.maketrans({
            r"{": r"{{",
            r"}": r"}}",
            "-":  r"\-",
            "]":  r"\]",
            "\\": r"\\",
            "^":  r"\^",
            "$":  r"\$",
            "*":  r"\*",
            ".":  r"\.",
        }))
    }