import enum
import re
import typing as tp

from .args import split_args

# consts
TypParsed = tp.Tuple[str, str]
TypParseFunc = tp.Callable[[str, str], TypParsed]

_COMMAND_REGISTRY: tp.Dict[str, TypParseFunc] = {}
_SEPARATORS = ['&', '&&', '|', '||', '>', '>>', '<']
_RE_DRIVE = re.compile(r'[A-Za-z]:\\')


class PathState(enum.Enum):
    START_NEW = 1
    END_CURRENT = 2
    CONTINUE = 3


TypPathJudge = tp.Literal[PathState.START_NEW, PathState.END_CURRENT, PathState.CONTINUE]


def get_parse_func(name: str) -> tp.Optional[TypParseFunc]:
    if name in _SEPARATORS:
        return _parse_separator(name)
    elif name in _COMMAND_REGISTRY:
        return _COMMAND_REGISTRY[name]
    return None


def command(names: tp.List[str]):
    """command register"""

    def decorator(func):
        for name in names:
            _COMMAND_REGISTRY[name] = func
        return func

    return decorator


@command(names=['cd'])
def parse_cd(text: str, kind: str) -> TypParsed:
    """
    Change Directory - Select a Folder (and drive)

    Syntax
      CD [/D] [drive:][path]
      CD [../..]
    """

    def path_judge(p: str) -> PathState:
        if p.startswith('/'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if '/d' in args:
        args.remove('/d')
    if kind == 'cmd':
        return f'cd /d {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'cd {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


@command(names=['copy'])
def parse_copy(text: str, kind: str) -> TypParsed:
    """
    Copy one or more files to another location.

    Syntax
      COPY [options] [/A|/B] source [/A|/B] [+ source2 [/A|/B]...] [destination [/A|/B]]

      COPY source1 + source2 destination [options]
    """

    def path_judge(p: str) -> PathState:
        if p.startswith('/') or p == '+':
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if kind == 'cmd':
        return f'copy {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'cp {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


@command(names=['cp'])
def parse_cp(text: str, kind: str) -> TypParsed:
    """
    Unix "copy"
    """

    def path_judge(p: str) -> PathState:
        if p.startswith('/') or p == '+' or p.startswith('-'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if kind == 'cmd':
        if '-r' in args:
            cmd_prefix = 'robocopy /e'
            args.remove('-r')
        else:
            cmd_prefix = 'copy'
        return f'{cmd_prefix} {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'cp {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


@command(names=['del'])
def parse_del(text: str, kind: str) -> TypParsed:
    """
    Delete one or more files.

    Syntax
      DEL [options] [/A:file_attributes] files_to_delete
    """

    def path_judge(p: str) -> PathState:
        if p.startswith('/'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if kind == 'cmd':
        return f'del {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'rm {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


@command(names=['dir', 'ls'])
def parse_dir(text: str, kind: str) -> TypParsed:
    """
    Display a list of files and subfolders.

    Syntax
      DIR [pathname] [options]
      DIR [options] [pathname]
    """

    def path_judge(p: str) -> PathState:
        if p.startswith('/'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if kind == 'cmd':
        return f'dir {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'ls {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


@command(names=['move', 'mv'])
def parse_move(text: str, kind: str) -> TypParsed:
    """
    Move a file from one folder to another.

    Syntax
      MOVE [options] [Source] [Target]
    """

    def path_judge(p: str) -> PathState:
        if p.startswith('/'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if kind == 'cmd':
        return f'move {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'mv {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


@command(names=['type', 'cat'])
def parse_type(text: str, kind: str) -> TypParsed:
    """
    Display the contents of one or more text files.

    Syntax
      TYPE [drive:]pathname
      TYPE [drive:]pathname [drive:]pathname
    """

    def path_judge(p: str) -> PathState:
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=path_judge)
    if kind == 'cmd':
        return f'type {" ".join(args)}', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return f'cat {" ".join(args)}', remaining
    raise ValueError(f'unknown command kind: {kind}')


def _parse_separator(name: str) -> tp.Optional[TypParseFunc]:
    """separators"""

    def inner(text: str, kind: str):
        return name, text

    return inner


def _parse_common(
        text: str,
        classify: tp.Callable[[str], TypPathJudge],
) -> tp.Tuple[tp.List[str], str]:
    """Shared arg-parsing skeleton used by every registered command.

    Args:
        text:           raw argument string after the command name.
        classify:       callback that returns judge path state for a given token.
    """
    assert text
    parts = split_args(text)
    args: tp.List[str] = []
    in_pathname = False
    contain_tail = True
    i = 0
    for i, p in enumerate(parts):
        if p in _SEPARATORS:
            contain_tail = False
            break

        kind = classify(p)

        if not in_pathname and kind == PathState.START_NEW:
            in_pathname = True
            args.append(p)
        elif not in_pathname and kind == PathState.END_CURRENT:
            if p in _COMMAND_REGISTRY:
                contain_tail = False
                break
            args.append(p)
        elif not in_pathname and kind == PathState.CONTINUE:
            if p in _COMMAND_REGISTRY:
                contain_tail = False
                break
            args.append(p)
        elif in_pathname and kind == PathState.START_NEW:
            # close current path, start a new one
            args[-1] = f'"{args[-1]}"'
            args.append(p)
        elif in_pathname and kind == PathState.CONTINUE:
            args[-1] += f' {p}'
        elif in_pathname and kind == PathState.END_CURRENT:
            in_pathname = False
            args[-1] = f'"{args[-1]}"'
            args.append(p)

    if in_pathname:
        args[-1] = f'"{args[-1]}"'

    remaining = parts[i + 1:] if contain_tail else parts[i:]
    return args, " ".join(remaining)


def win_path_to_unix(arg: str) -> str:
    if not _RE_DRIVE.search(arg):
        return arg
    arg_strip = arg.strip('\"\'')
    drive = arg_strip[0].lower()
    unix_path = arg_strip[3:].replace('\\', '/')
    return f'"/{drive}/{unix_path}"'
