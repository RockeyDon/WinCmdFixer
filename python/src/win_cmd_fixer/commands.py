import enum
import re
import typing as tp

from .args import split_args

# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------
TypParsed = tp.Tuple[str, str]
TypParseFunc = tp.Callable[[str, str], TypParsed]

_COMMAND_REGISTRY: tp.Dict[str, TypParseFunc] = {}

# CMD / PS5 separators.  '&&' and '||' are CMD-only; PS5 uses ';'.
_SEPARATORS = ['&', '&&', '|', '||', '>', '>>', '<']

_RE_DRIVE = re.compile(r'[A-Za-z]:\\')

# Escape characters per shell kind
_ESCAPE_CHARS: tp.Dict[str, str] = {
    'cmd': '^',
    'powershell': '`',
    'unix': '\\',
}


class PathState(enum.Enum):
    START_NEW = 1
    END_CURRENT = 2
    CONTINUE = 3


TypPathJudge = tp.Literal[PathState.START_NEW, PathState.END_CURRENT, PathState.CONTINUE]


def get_parse_func(name: str) -> tp.Optional[TypParseFunc]:
    if name in _SEPARATORS:
        return _parse_separator(name)
    if name in _COMMAND_REGISTRY:
        return _COMMAND_REGISTRY[name]
    return None


def command(names: tp.List[str]):
    """Register a parse function under one or more command names."""

    def decorator(func: TypParseFunc) -> TypParseFunc:
        for n in names:
            _COMMAND_REGISTRY[n] = func
        return func

    return decorator


# ---------------------------------------------------------------------------
# Separator handling
# ---------------------------------------------------------------------------

# Map separators from CMD style to PowerShell 5.x equivalents.
_PS_SEPARATOR_MAP: tp.Dict[str, str] = {
    '&&': ';',
    '||': ';',   # rough equivalent; exact semantics differ
    '&': ';',
}


def _translate_separator(sep: str, kind: str) -> str:
    """Return the shell-appropriate separator."""
    if kind == 'powershell':
        return _PS_SEPARATOR_MAP.get(sep, sep)
    return sep


def _parse_separator(name: str) -> TypParseFunc:
    """Return a parse function that emits a separator token."""

    def inner(text: str, kind: str) -> TypParsed:
        return _translate_separator(name, kind), text

    return inner


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _fmt_cmd(name: str, args: tp.List[str]) -> str:
    """Format ``name arg1 arg2 ...``, avoiding a trailing space when *args*
    is empty."""
    if args:
        return f'{name} {" ".join(args)}'
    return name


def _parse_common(
        text: str,
        classify: tp.Callable[[str], PathState],
) -> tp.Tuple[tp.List[str], str]:
    """Shared arg-parsing skeleton used by every registered command.

    Args:
        text:     raw argument string after the command name (may be empty).
        classify: callback that judges how a token relates to path parsing.
    """
    if not text or not text.strip():
        return [], ''

    # Input is always Windows-style (broken CMD), so always parse with '^'.
    parts = split_args(text, escape_char='^')
    args: tp.List[str] = []
    in_pathname = False
    contain_tail = True
    i = 0

    for i, p in enumerate(parts):
        if p in _SEPARATORS:
            contain_tail = False
            break

        state = classify(p)

        if not in_pathname and state == PathState.START_NEW:
            in_pathname = True
            args.append(p)
        elif not in_pathname and state == PathState.END_CURRENT:
            if p in _COMMAND_REGISTRY:
                contain_tail = False
                break
            args.append(p)
        elif not in_pathname and state == PathState.CONTINUE:
            if p in _COMMAND_REGISTRY:
                contain_tail = False
                break
            args.append(p)
        elif in_pathname and state == PathState.START_NEW:
            args[-1] = f'"{args[-1]}"'
            args.append(p)
        elif in_pathname and state == PathState.CONTINUE:
            args[-1] += f' {p}'
        elif in_pathname and state == PathState.END_CURRENT:
            in_pathname = False
            args[-1] = f'"{args[-1]}"'
            args.append(p)

    if in_pathname:
        args[-1] = f'"{args[-1]}"'

    remaining = parts[i + 1:] if contain_tail else parts[i:]
    return args, ' '.join(remaining)


def win_path_to_unix(arg: str) -> str:
    """Convert a Windows absolute path to a Unix-style mount path."""
    if not _RE_DRIVE.search(arg):
        return arg
    arg_strip = arg.strip('\"\'')
    drive = arg_strip[0].lower()
    unix_path = arg_strip[3:].replace('\\', '/')
    return f'"/{drive}/{unix_path}"'


# ---------------------------------------------------------------------------
# Standard path-judge helpers (reused across many commands)
# ---------------------------------------------------------------------------

def _judge_standard(p: str) -> PathState:
    """Options start with '/'; drive letters start a new path."""
    if p.startswith('/'):
        return PathState.END_CURRENT
    if _RE_DRIVE.search(p):
        return PathState.START_NEW
    return PathState.CONTINUE


def _judge_unix_opts(p: str) -> PathState:
    """Like standard but also treats '-xxx' as an option."""
    if p.startswith('/') or p.startswith('-'):
        return PathState.END_CURRENT
    if _RE_DRIVE.search(p):
        return PathState.START_NEW
    return PathState.CONTINUE


def _judge_no_option(p: str) -> PathState:
    """Only drive letters start a new path; nothing ends current."""
    if _RE_DRIVE.search(p):
        return PathState.START_NEW
    return PathState.CONTINUE


# ---------------------------------------------------------------------------
# Helper: remove a flag (case-insensitive) from args list
# ---------------------------------------------------------------------------

def _remove_flag_ci(args: tp.List[str], flag: str) -> bool:
    """Remove *flag* (case-insensitive) from *args*. Return True if found."""
    flag_lower = flag.lower()
    for idx, a in enumerate(args):
        if a.lower() == flag_lower:
            args.pop(idx)
            return True
    return False


# ---------------------------------------------------------------------------
# Command definitions
# ---------------------------------------------------------------------------

@command(names=['cd'])
def parse_cd(text: str, kind: str) -> TypParsed:
    """
    Change Directory.

    CMD:  CD [/D] drive:\\path
    PS:   Set-Location [-Path] path
    Unix: cd path
    """
    args, remaining = _parse_common(text, classify=_judge_standard)
    _remove_flag_ci(args, '/d')

    if kind == 'cmd':
        prefix = 'cd /d' if args else 'cd'
        return _fmt_cmd(prefix, args), remaining
    if kind == 'powershell':
        return _fmt_cmd('Set-Location', args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('cd', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['copy'])
def parse_copy(text: str, kind: str) -> TypParsed:
    """
    Copy files.

    CMD:  COPY [/A|/B] source [+ source2 ...] destination
    PS:   Copy-Item -Path src -Destination dst
    Unix: cp src dst
    """

    def judge(p: str) -> PathState:
        if p.startswith('/') or p == '+':
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=judge)

    if kind == 'cmd':
        return _fmt_cmd('copy', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/') and a != '+']
        return _fmt_cmd('Copy-Item', ps_args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('cp', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['cp'])
def parse_cp(text: str, kind: str) -> TypParsed:
    """Unix-style copy."""

    def judge(p: str) -> PathState:
        if p.startswith('/') or p == '+' or p.startswith('-'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    args, remaining = _parse_common(text, classify=judge)

    if kind == 'cmd':
        if '-r' in args:
            cmd_prefix = 'robocopy /e'
            args.remove('-r')
        else:
            cmd_prefix = 'copy'
        return _fmt_cmd(cmd_prefix, args), remaining
    if kind == 'powershell':
        recurse = '-r' in args
        if recurse:
            args.remove('-r')
        suffix = ' -Recurse' if recurse else ''
        return _fmt_cmd('Copy-Item', args) + suffix, remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('cp', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['del'])
def parse_del(text: str, kind: str) -> TypParsed:
    """
    Delete files.

    CMD:  DEL [/P] files
    PS:   Remove-Item path
    Unix: rm path
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('del', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        return _fmt_cmd('Remove-Item', ps_args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('rm', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['rm'])
def parse_rm(text: str, kind: str) -> TypParsed:
    """
    Unix-style remove.

    CMD:  del / rmdir /s /q (when -rf)
    PS:   Remove-Item [-Recurse] [-Force]
    Unix: rm path
    """
    args, remaining = _parse_common(text, classify=_judge_unix_opts)

    has_r = _remove_flag_ci(args, '-r')
    has_f = _remove_flag_ci(args, '-f')
    has_rf = _remove_flag_ci(args, '-rf')
    recursive = has_r or has_rf
    force = has_f or has_rf

    if kind == 'cmd':
        if recursive:
            flags = '/s'
            if force:
                flags += ' /q'
            return _fmt_cmd(f'rmdir {flags}', args), remaining
        return _fmt_cmd('del', args), remaining
    if kind == 'powershell':
        suffix = ''
        if recursive:
            suffix += ' -Recurse'
        if force:
            suffix += ' -Force'
        return _fmt_cmd('Remove-Item', args) + suffix, remaining
    if kind == 'unix':
        flags = ''
        if recursive:
            flags += '-r'
        if force:
            flags += 'f' if flags else '-f'
        args = [win_path_to_unix(a) for a in args]
        if flags:
            return _fmt_cmd(f'rm {flags}', args), remaining
        return _fmt_cmd('rm', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['dir', 'ls'])
def parse_dir(text: str, kind: str) -> TypParsed:
    """
    List directory contents.

    CMD:  DIR [/P] path
    PS:   Get-ChildItem path
    Unix: ls path
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('dir', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        return _fmt_cmd('Get-ChildItem', ps_args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('ls', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['move', 'mv'])
def parse_move(text: str, kind: str) -> TypParsed:
    """
    Move / rename files.

    CMD:  MOVE [/Y] source target
    PS:   Move-Item -Path src -Destination dst
    Unix: mv src dst
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('move', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        return _fmt_cmd('Move-Item', ps_args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('mv', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['type', 'cat'])
def parse_type(text: str, kind: str) -> TypParsed:
    """
    Display file contents.

    CMD:  TYPE file
    PS:   Get-Content file
    Unix: cat file
    """
    args, remaining = _parse_common(text, classify=_judge_no_option)

    if kind == 'cmd':
        return _fmt_cmd('type', args), remaining
    if kind == 'powershell':
        return _fmt_cmd('Get-Content', args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('cat', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['mkdir', 'md'])
def parse_mkdir(text: str, kind: str) -> TypParsed:
    """
    Create directory.

    CMD:  MKDIR path
    PS:   New-Item -ItemType Directory -Path path
    Unix: mkdir path
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('mkdir', args), remaining
    if kind == 'powershell':
        return _fmt_cmd('New-Item -ItemType Directory -Path', args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('mkdir', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['rmdir', 'rd'])
def parse_rmdir(text: str, kind: str) -> TypParsed:
    """
    Remove directory.

    CMD:  RMDIR [/S] [/Q] path
    PS:   Remove-Item path -Recurse
    Unix: rmdir path  /  rm -r path
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('rmdir', args), remaining
    if kind == 'powershell':
        has_s = _remove_flag_ci(args, '/s')
        _remove_flag_ci(args, '/q')
        ps_args = [a for a in args if not a.startswith('/')]
        suffix = ' -Recurse -Force' if has_s else ''
        return _fmt_cmd('Remove-Item', ps_args) + suffix, remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('rmdir', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['rename', 'ren'])
def parse_rename(text: str, kind: str) -> TypParsed:
    """
    Rename a file or directory.

    CMD:  REN old new
    PS:   Rename-Item -Path old -NewName new
    Unix: mv old new

    Note: the second argument is always a simple filename (no path).
    Once the first path ends, the next token is the new name.
    """

    def judge(p: str) -> PathState:
        if p.startswith('/'):
            return PathState.END_CURRENT
        if _RE_DRIVE.search(p):
            return PathState.START_NEW
        return PathState.CONTINUE

    if not text or not text.strip():
        if kind == 'powershell':
            return 'Rename-Item', ''
        if kind == 'unix':
            return 'mv', ''
        return 'ren', ''

    parts = split_args(text, escape_char='^')
    args: tp.List[str] = []
    in_pathname = False
    first_path_done = False
    remaining_parts: tp.List[str] = []
    hit_sep = False

    for i, p in enumerate(parts):
        if p in _SEPARATORS:
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
            remaining_parts = parts[i:]
            hit_sep = True
            break

        if first_path_done:
            # After the first path, everything is the new name (a simple token)
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
            args.append(p)
            continue

        state = judge(p)

        if not in_pathname and state == PathState.START_NEW:
            in_pathname = True
            args.append(p)
        elif not in_pathname and state == PathState.END_CURRENT:
            args.append(p)
        elif not in_pathname and state == PathState.CONTINUE:
            args.append(p)
        elif in_pathname and state == PathState.START_NEW:
            args[-1] = f'"{args[-1]}"'
            first_path_done = True
            args.append(p)
            in_pathname = True
        elif in_pathname and state == PathState.CONTINUE:
            # Check if this could be the new name (non-path token following a path)
            # Heuristic: if the token has no backslash and no drive letter, it's
            # likely the new filename, not a path continuation.
            if '\\' not in p and not _RE_DRIVE.search(p) and '/' not in p:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
                first_path_done = True
                args.append(p)
            else:
                args[-1] += f' {p}'
        elif in_pathname and state == PathState.END_CURRENT:
            in_pathname = False
            args[-1] = f'"{args[-1]}"'
            first_path_done = True
            args.append(p)

    if in_pathname:
        args[-1] = f'"{args[-1]}"'

    remaining = ' '.join(remaining_parts)

    if kind == 'cmd':
        return _fmt_cmd('ren', args), remaining
    if kind == 'powershell':
        return _fmt_cmd('Rename-Item', args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('mv', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['echo'])
def parse_echo(text: str, kind: str) -> TypParsed:
    """
    Display a message.

    CMD:  ECHO message
    PS:   Write-Output message
    Unix: echo message
    """
    # echo is special: everything after the command name is the message,
    # up to the first separator.  We must not strip quotes from the raw text.
    if not text or not text.strip():
        return ('echo', '') if kind != 'powershell' else ('Write-Output', '')

    # We manually scan for separators in the raw text instead of using
    # split_args, so that quoted strings are preserved as-is.
    msg_parts: tp.List[str] = []
    rest_parts: tp.List[str] = []
    tokens = text.split()
    hit_sep = False

    for t in tokens:
        if t in _SEPARATORS and not hit_sep:
            hit_sep = True
        if hit_sep:
            rest_parts.append(t)
        else:
            msg_parts.append(t)

    message = ' '.join(msg_parts)
    remaining = ' '.join(rest_parts)

    if kind == 'cmd':
        return f'echo {message}', remaining
    if kind == 'powershell':
        return f'Write-Output {message}', remaining
    if kind == 'unix':
        return f'echo {message}', remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['find'])
def parse_find(text: str, kind: str) -> TypParsed:
    """
    CMD FIND - search for a text string in a file.

    CMD:  FIND [/I] "string" file
    PS:   Select-String -Pattern "string" -Path file
    Unix: grep "string" file

    The quoted search pattern must be preserved as-is.
    """
    if not text or not text.strip():
        if kind == 'powershell':
            return 'Select-String', ''
        if kind == 'unix':
            return 'grep', ''
        return 'find', ''

    # Split raw text preserving quotes for the search pattern.
    tokens = text.split()
    args: tp.List[str] = []
    remaining_parts: tp.List[str] = []
    hit_sep = False
    # Track path building state
    in_pathname = False

    for t in tokens:
        if hit_sep:
            remaining_parts.append(t)
            continue
        if t in _SEPARATORS:
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
            hit_sep = True
            remaining_parts.append(t)
            continue

        # Quoted string (search pattern) or option
        if t.startswith('"') or t.startswith('/'):
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
            args.append(t)
        elif _RE_DRIVE.search(t):
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
            in_pathname = True
            args.append(t)
        else:
            if in_pathname:
                args[-1] += f' {t}'
            else:
                args.append(t)

    if in_pathname:
        args[-1] = f'"{args[-1]}"'

    remaining = ' '.join(remaining_parts)

    if kind == 'cmd':
        return _fmt_cmd('find', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        return _fmt_cmd('Select-String', ps_args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('grep', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['findstr', 'grep'])
def parse_findstr(text: str, kind: str) -> TypParsed:
    """
    Search for strings in files (regex capable).

    CMD:  FINDSTR [/R] "pattern" files
    PS:   Select-String -Pattern "pattern" -Path files
    Unix: grep "pattern" files

    The quoted search pattern must be preserved as-is.
    """
    if not text or not text.strip():
        if kind == 'powershell':
            return 'Select-String', ''
        if kind == 'unix':
            return 'grep', ''
        return 'findstr', ''

    # Same approach as parse_find: manual scanning to preserve quotes.
    tokens = text.split()
    args: tp.List[str] = []
    remaining_parts: tp.List[str] = []
    hit_sep = False
    in_pathname = False

    for t in tokens:
        if hit_sep:
            remaining_parts.append(t)
            continue
        if t in _SEPARATORS:
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
            hit_sep = True
            remaining_parts.append(t)
            continue

        if t.startswith('"') or t.startswith('/') or t.startswith('-'):
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
                in_pathname = False
            args.append(t)
        elif _RE_DRIVE.search(t):
            if in_pathname:
                args[-1] = f'"{args[-1]}"'
            in_pathname = True
            args.append(t)
        else:
            if in_pathname:
                args[-1] += f' {t}'
            else:
                args.append(t)

    if in_pathname:
        args[-1] = f'"{args[-1]}"'

    remaining = ' '.join(remaining_parts)

    if kind == 'cmd':
        return _fmt_cmd('findstr', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/') and not a.startswith('-')]
        return _fmt_cmd('Select-String', ps_args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('grep', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['cls', 'clear'])
def parse_cls(text: str, kind: str) -> TypParsed:
    """
    Clear the screen.

    CMD:  CLS
    PS:   Clear-Host
    Unix: clear
    """
    remaining = text.strip() if text else ''
    if kind == 'cmd':
        return 'cls', remaining
    if kind == 'powershell':
        return 'Clear-Host', remaining
    if kind == 'unix':
        return 'clear', remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['more'])
def parse_more(text: str, kind: str) -> TypParsed:
    """
    Display output one screen at a time.

    CMD:  MORE file
    PS:   Get-Content file | Out-Host -Paging
    Unix: more file
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('more', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        ps_str = ' '.join(ps_args)
        return f'Get-Content {ps_str} | Out-Host -Paging' if ps_str else 'Get-Content | Out-Host -Paging', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('more', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['xcopy'])
def parse_xcopy(text: str, kind: str) -> TypParsed:
    """
    Extended copy (directories).

    CMD:  XCOPY source destination [/S] [/E]
    PS:   Copy-Item -Recurse
    Unix: cp -r
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('xcopy', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        return _fmt_cmd('Copy-Item', ps_args) + ' -Recurse', remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('cp -r', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['pushd'])
def parse_pushd(text: str, kind: str) -> TypParsed:
    """
    Push directory onto stack and change to it.

    CMD:  PUSHD path
    PS:   Push-Location path
    Unix: pushd path
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('pushd', args), remaining
    if kind == 'powershell':
        return _fmt_cmd('Push-Location', args), remaining
    if kind == 'unix':
        args = [win_path_to_unix(a) for a in args]
        return _fmt_cmd('pushd', args), remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['popd'])
def parse_popd(text: str, kind: str) -> TypParsed:
    """
    Pop directory from stack.

    CMD:  POPD
    PS:   Pop-Location
    Unix: popd
    """
    remaining = text.strip() if text else ''
    if kind == 'cmd':
        return 'popd', remaining
    if kind == 'powershell':
        return 'Pop-Location', remaining
    if kind == 'unix':
        return 'popd', remaining
    raise ValueError(f'unknown kind: {kind}')


@command(names=['where', 'which'])
def parse_where(text: str, kind: str) -> TypParsed:
    """
    Locate a program file.

    CMD:  WHERE name
    PS:   Get-Command name
    Unix: which name
    """
    args, remaining = _parse_common(text, classify=_judge_standard)

    if kind == 'cmd':
        return _fmt_cmd('where', args), remaining
    if kind == 'powershell':
        ps_args = [a for a in args if not a.startswith('/')]
        return _fmt_cmd('Get-Command', ps_args), remaining
    if kind == 'unix':
        return _fmt_cmd('which', args), remaining
    raise ValueError(f'unknown kind: {kind}')
