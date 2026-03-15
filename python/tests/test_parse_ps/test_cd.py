from src.win_cmd_fixer import fix_powershell

test_cases = [
    # basic
    {
        'input': 'cd D:\\Program Files\\',
        'expected': 'Set-Location "D:\\Program Files\\"'
    },
    {
        'input': 'cd "D:\\Program Files\\"',
        'expected': 'Set-Location "D:\\Program Files\\"'
    },
    {
        'input': 'CD "D:\\Program Files\\"',
        'expected': 'Set-Location "D:\\Program Files\\"'
    },
    # /d flag should be removed
    {
        'input': 'cd /d D:\\Program Files\\',
        'expected': 'Set-Location "D:\\Program Files\\"'
    },
    {
        'input': 'cd /D D:\\Program Files\\',
        'expected': 'Set-Location "D:\\Program Files\\"'
    },
    # && separator -> ;
    {
        'input': 'cd D:\\Program Files\\ && cd C:\\Program Files\\',
        'expected': 'Set-Location "D:\\Program Files\\" ; Set-Location "C:\\Program Files\\"'
    },
    # || separator -> ;
    {
        'input': 'cd D:\\Program Files\\ || cd C:\\Program Files\\',
        'expected': 'Set-Location "D:\\Program Files\\" ; Set-Location "C:\\Program Files\\"'
    },
    # pipe (unchanged)
    {
        'input': 'cd D:\\Program Files\\ | cd C:\\Program Files\\',
        'expected': 'Set-Location "D:\\Program Files\\" | Set-Location "C:\\Program Files\\"'
    },
    # redirect (unchanged)
    {
        'input': 'cd D:\\Program Files\\ > results.txt',
        'expected': 'Set-Location "D:\\Program Files\\" > results.txt'
    },
]


def test_parse_cd():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
