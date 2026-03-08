from .commands import get_parse_func


def fix_cmd(text: str) -> str:
    """convert for cmd"""
    return _parser(text, 'cmd')


def fix_unix_shell(text: str) -> str:
    """convert for unix-like shell"""
    return _parser(text, 'unix')


def _parser(text: str, kind: str) -> str:
    """main function"""
    remaining = text
    output = []
    while remaining:
        try:
            first, others = remaining.split(' ', 1)
        except ValueError:
            output.append(remaining)  # Cannot split anymore
            break
        if parse_func := get_parse_func(first.lower()):
            first_cmd, remaining = parse_func(others, kind)
            output.append(first_cmd)
        else:
            output.append(remaining)  # Cannot parse {first} yet, I'm developing...
            break
    return ' '.join(output)
