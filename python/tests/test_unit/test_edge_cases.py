from src.win_cmd_fixer import fix_cmd, fix_powershell, fix_unix_shell


# ---------------------------------------------------------------
# 1. Already-correct commands should pass through unchanged
# ---------------------------------------------------------------
correct_cmd_cases = [
    # correct CMD
    {'input': 'cd /d "D:\\Program Files\\"',  'expected': 'cd /d "D:\\Program Files\\"'},
    {'input': 'dir "D:\\Program Files\\"',     'expected': 'dir "D:\\Program Files\\"'},
    {'input': 'copy "D:\\a.txt" "C:\\b.txt"',  'expected': 'copy "D:\\a.txt" "C:\\b.txt"'},
    {'input': 'del "D:\\Program Files\\a.txt"', 'expected': 'del "D:\\Program Files\\a.txt"'},
    {'input': 'move "D:\\a.txt" "C:\\b.txt"',  'expected': 'move "D:\\a.txt" "C:\\b.txt"'},
    {'input': 'type "D:\\Program Files\\a.txt"', 'expected': 'type "D:\\Program Files\\a.txt"'},
    {'input': 'mkdir "D:\\Program Files\\New"', 'expected': 'mkdir "D:\\Program Files\\New"'},
    {'input': 'rmdir /S /Q "D:\\Program Files\\Old"', 'expected': 'rmdir /S /Q "D:\\Program Files\\Old"'},
    {'input': 'ren "D:\\Program Files\\old.txt" new.txt', 'expected': 'ren "D:\\Program Files\\old.txt" new.txt'},
    {'input': 'echo hello world',              'expected': 'echo hello world'},
    {'input': 'cls',                           'expected': 'cls'},
    {'input': 'popd',                          'expected': 'popd'},
    {'input': 'where python',                  'expected': 'where python'},
    {'input': 'pushd "D:\\Program Files\\"',   'expected': 'pushd "D:\\Program Files\\"'},
    {'input': 'find "hello" "D:\\a.txt"',      'expected': 'find "hello" "D:\\a.txt"'},
    {'input': 'findstr /R "pattern" "D:\\a.txt"', 'expected': 'findstr /R "pattern" "D:\\a.txt"'},
    {'input': 'more "D:\\Program Files\\a.txt"', 'expected': 'more "D:\\Program Files\\a.txt"'},
    {'input': 'xcopy /S "D:\\a" "D:\\b"',      'expected': 'xcopy /S "D:\\a" "D:\\b"'},
]


def test_correct_cmd_passthrough():
    for ind, case in enumerate(correct_cmd_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


correct_ps_cases = [
    {'input': 'Set-Location "D:\\Program Files\\"', 'expected': 'Set-Location "D:\\Program Files\\"'},
    {'input': 'Get-ChildItem "D:\\Program Files\\"', 'expected': 'Get-ChildItem "D:\\Program Files\\"'},
    {'input': 'Copy-Item "D:\\a.txt" "C:\\b.txt"',   'expected': 'Copy-Item "D:\\a.txt" "C:\\b.txt"'},
    {'input': 'Remove-Item "D:\\a.txt"',              'expected': 'Remove-Item "D:\\a.txt"'},
    {'input': 'Move-Item "D:\\a.txt" "C:\\b.txt"',    'expected': 'Move-Item "D:\\a.txt" "C:\\b.txt"'},
    {'input': 'Get-Content "D:\\a.txt"',              'expected': 'Get-Content "D:\\a.txt"'},
    {'input': 'Clear-Host',                           'expected': 'Clear-Host'},
    {'input': 'Pop-Location',                         'expected': 'Pop-Location'},
    {'input': 'Get-Command python',                   'expected': 'Get-Command python'},
    {'input': 'Write-Output hello',                   'expected': 'Write-Output hello'},
]


def test_correct_ps_passthrough():
    for ind, case in enumerate(correct_ps_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


# ---------------------------------------------------------------
# 2. Empty / whitespace / no-arg commands: never crash
# ---------------------------------------------------------------
no_crash_cases_cmd = [
    {'input': '',       'expected': ''},
    {'input': '   ',    'expected': ''},
    {'input': 'cd',     'expected': 'cd'},
    {'input': 'cd ',    'expected': 'cd'},
    {'input': 'dir',    'expected': 'dir'},
    {'input': 'dir ',   'expected': 'dir'},
    {'input': 'del',    'expected': 'del'},
    {'input': 'copy',   'expected': 'copy'},
    {'input': 'move',   'expected': 'move'},
    {'input': 'type',   'expected': 'type'},
    {'input': 'cls',    'expected': 'cls'},
    {'input': 'cls ',   'expected': 'cls'},
    {'input': 'popd',   'expected': 'popd'},
    {'input': 'popd ',  'expected': 'popd'},
    {'input': 'mkdir',  'expected': 'mkdir'},
    {'input': 'rmdir',  'expected': 'rmdir'},
    {'input': 'echo',   'expected': 'echo'},
    {'input': 'more',   'expected': 'more'},
    {'input': 'pushd',  'expected': 'pushd'},
    {'input': 'where',  'expected': 'where'},
    {'input': 'find',   'expected': 'find'},
    {'input': 'findstr', 'expected': 'findstr'},
    {'input': 'xcopy',  'expected': 'xcopy'},
    {'input': 'rename', 'expected': 'ren'},
    {'input': 'ren',    'expected': 'ren'},
]


def test_no_crash_cmd():
    for ind, case in enumerate(no_crash_cases_cmd, start=1):
        result = fix_cmd(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


no_crash_cases_ps = [
    {'input': '',       'expected': ''},
    {'input': '   ',    'expected': ''},
    {'input': 'cd',     'expected': 'Set-Location'},
    {'input': 'dir',    'expected': 'Get-ChildItem'},
    {'input': 'del',    'expected': 'Remove-Item'},
    {'input': 'copy',   'expected': 'Copy-Item'},
    {'input': 'move',   'expected': 'Move-Item'},
    {'input': 'type',   'expected': 'Get-Content'},
    {'input': 'cls',    'expected': 'Clear-Host'},
    {'input': 'popd',   'expected': 'Pop-Location'},
    {'input': 'mkdir',  'expected': 'New-Item -ItemType Directory -Path'},
    {'input': 'echo',   'expected': 'Write-Output'},
    {'input': 'pushd',  'expected': 'Push-Location'},
    {'input': 'where',  'expected': 'Get-Command'},
]


def test_no_crash_ps():
    for ind, case in enumerate(no_crash_cases_ps, start=1):
        result = fix_powershell(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


no_crash_cases_unix = [
    {'input': '',       'expected': ''},
    {'input': '   ',    'expected': ''},
    {'input': 'cd',     'expected': 'cd'},
    {'input': 'dir',    'expected': 'ls'},
    {'input': 'del',    'expected': 'rm'},
    {'input': 'copy',   'expected': 'cp'},
    {'input': 'move',   'expected': 'mv'},
    {'input': 'type',   'expected': 'cat'},
    {'input': 'cls',    'expected': 'clear'},
    {'input': 'popd',   'expected': 'popd'},
]


def test_no_crash_unix():
    for ind, case in enumerate(no_crash_cases_unix, start=1):
        result = fix_unix_shell(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


# ---------------------------------------------------------------
# 3. Totally unknown commands: pass through unchanged
# ---------------------------------------------------------------
unknown_cases = [
    {'input': 'someunknown arg1 arg2',  'expected': 'someunknown arg1 arg2'},
    {'input': 'notacmd',                'expected': 'notacmd'},
    {'input': 'foo bar baz',            'expected': 'foo bar baz'},
]


def test_unknown_passthrough():
    for ind, case in enumerate(unknown_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


# ---------------------------------------------------------------
# 4. Unknown command before separator, known command after
# ---------------------------------------------------------------
skip_to_separator_cases = [
    {
        'input': 'echo hello && cd D:\\Program Files\\',
        'expected': 'echo hello && cd /d "D:\\Program Files\\"'
    },
    {
        'input': 'echo hello && type D:\\Program Files\\file.txt',
        'expected': 'echo hello && type "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'echo hello && echo world && dir D:\\Program Files\\',
        'expected': 'echo hello && echo world && dir "D:\\Program Files\\"'
    },
    {
        'input': 'foo bar | dir D:\\Program Files\\',
        'expected': 'foo bar | dir "D:\\Program Files\\"'
    },
]


def test_skip_to_separator():
    for ind, case in enumerate(skip_to_separator_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )


# ---------------------------------------------------------------
# 5. cd /D case-insensitive
# ---------------------------------------------------------------
cd_flag_cases = [
    {'input': 'cd /D D:\\Program Files\\', 'expected': 'cd /d "D:\\Program Files\\"'},
    {'input': 'cd /d D:\\Program Files\\', 'expected': 'cd /d "D:\\Program Files\\"'},
]


def test_cd_flag_case_insensitive():
    for ind, case in enumerate(cd_flag_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case['expected']
        assert result == expected, (
            f"Case {ind} failed: {case['input']!r} => {result!r}, expected {expected!r}"
        )
