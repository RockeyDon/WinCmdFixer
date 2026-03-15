from src.win_cmd_fixer import fix_powershell

test_cases = [
    # basic
    {
        'input': 'dir D:\\Program Files\\',
        'expected': 'Get-ChildItem "D:\\Program Files\\"'
    },
    {
        'input': 'dir "D:\\Program Files\\"',
        'expected': 'Get-ChildItem "D:\\Program Files\\"'
    },
    # ls alias
    {
        'input': 'ls D:\\Program Files\\',
        'expected': 'Get-ChildItem "D:\\Program Files\\"'
    },
    # && -> ;
    {
        'input': 'dir D:\\Program Files\\ && dir C:\\Program Files\\',
        'expected': 'Get-ChildItem "D:\\Program Files\\" ; Get-ChildItem "C:\\Program Files\\"'
    },
]


def test_parse_dir():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
