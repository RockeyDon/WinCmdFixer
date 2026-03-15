from .commands import get_parse_func, _SEPARATORS


def fix_cmd(text: str) -> str:
    """Convert a (possibly broken) command string into valid CMD syntax."""
    return _parser(text, 'cmd')


def fix_powershell(text: str) -> str:
    """Convert a (possibly broken) command string into valid PowerShell 5.x syntax."""
    return _parser(text, 'powershell')


def fix_unix_shell(text: str) -> str:
    """Convert a (possibly broken) command string into valid Unix shell syntax."""
    return _parser(text, 'unix')


def _parser(text: str, kind: str) -> str:
    """Main parsing loop.

    Splits *text* by the first whitespace to identify a command name, then
    delegates to the registered parse function.  When a command is not
    recognised, it is emitted verbatim and the parser continues to look for
    separators so that subsequent commands can still be fixed.
    """
    remaining = text.strip()
    output: list[str] = []

    while remaining:
        # Split into first token and the rest
        parts = remaining.split(None, 1)
        first = parts[0]
        others = parts[1] if len(parts) > 1 else ''

        parse_func = get_parse_func(first.lower())

        if parse_func is not None:
            parsed_cmd, remaining = parse_func(others, kind)
            output.append(parsed_cmd)
            remaining = remaining.strip()
        else:
            # Unknown command: emit it, then scan forward for a separator
            # so that the rest of the pipeline can still be processed.
            output.append(first)
            remaining = others.strip()
            remaining = _skip_to_separator(remaining, output)

    return ' '.join(output)


def _skip_to_separator(text: str, output: list[str]) -> str:
    """Consume tokens until a separator is found, appending them to *output*.

    Returns the remaining text (starting from the separator token itself so
    the main loop can handle it).
    """
    remaining = text
    while remaining:
        parts = remaining.split(None, 1)
        token = parts[0]
        rest = parts[1] if len(parts) > 1 else ''

        if token in _SEPARATORS:
            # Found a separator; leave it for the main loop
            return remaining
        # Also check for two-char separators that may start the string
        for sep in ('&&', '||', '>>', '<<'):
            if remaining.startswith(sep):
                return remaining

        output.append(token)
        remaining = rest.strip()

    return ''
