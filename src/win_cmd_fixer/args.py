import typing as tp


def split_args(text: str) -> tp.List[str]:
    """split by space, but keep ones in quotes"""
    result = []
    current = []
    in_quotes = False
    escaped = False
    quote_char = None

    i = 0
    while i < len(text):
        char = text[i]

        if char == '^' and not escaped:
            escaped = True
            i += 1
            continue
        if escaped:
            current.append(char)
            escaped = False
            i += 1
            continue
        if char in ('"', "'") and not in_quotes:
            in_quotes = True
            quote_char = char
            i += 1
            continue
        if char == quote_char and in_quotes:
            in_quotes = False
            quote_char = None
            i += 1
            if not current:
                result.append('')
            continue
        if char.isspace() and not in_quotes:
            if current:
                result.append(''.join(current))
                current = []
            i += 1
            continue
        current.append(char)
        i += 1
    # last one
    if current:
        result.append(''.join(current))
    return result
