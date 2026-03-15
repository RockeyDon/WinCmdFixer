from src.win_cmd_fixer import fix_powershell

test_cases = [
    # type -> Get-Content
    {
        'input': 'type D:\\Program Files\\file.txt',
        'expected': 'Get-Content "D:\\Program Files\\file.txt"'
    },
    # cat -> Get-Content
    {
        'input': 'cat D:\\Program Files\\file.txt',
        'expected': 'Get-Content "D:\\Program Files\\file.txt"'
    },
    # && -> ;
    {
        'input': 'type D:\\Program Files\\a.txt && type D:\\Program Files\\b.txt',
        'expected': 'Get-Content "D:\\Program Files\\a.txt" ; Get-Content "D:\\Program Files\\b.txt"'
    },
]


def test_parse_type():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
