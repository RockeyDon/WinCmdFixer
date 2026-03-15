import typing as tp


def split_args(text: str, escape_char: str = '^') -> tp.List[str]:
    """Split by space, but keep tokens inside quotes together.

    Args:
        text:        raw argument string.
        escape_char: shell-specific escape character
                     ('^' for CMD, '`' for PowerShell, '\\' for Unix).
    """
    result: tp.List[str] = []
    current: tp.List[str] = []
    in_quotes = False
    escaped = False
    quote_char: tp.Optional[str] = None

    i = 0
    while i < len(text):
        char = text[i]

        if char == escape_char and not escaped:
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

    # last token
    if current:
        result.append(''.join(current))
    return result
