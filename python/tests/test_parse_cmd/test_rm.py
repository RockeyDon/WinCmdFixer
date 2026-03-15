from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic: rm -> del
    {
        'input': 'rm D:\\Program Files\\file.txt',
        'expected': 'del "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'rm "D:\\Program Files\\file.txt"',
        'expected': 'del "D:\\Program Files\\file.txt"'
    },
    # rm -rf -> rmdir /s /q
    {
        'input': 'rm -rf D:\\Program Files\\OldFolder',
        'expected': 'rmdir /s /q "D:\\Program Files\\OldFolder"'
    },
    {
        'input': 'rm -rf "D:\\Program Files\\OldFolder"',
        'expected': 'rmdir /s /q "D:\\Program Files\\OldFolder"'
    },
    # rm -r (recursive but not forced)
    {
        'input': 'rm -r D:\\Program Files\\OldFolder',
        'expected': 'rmdir /s "D:\\Program Files\\OldFolder"'
    },
]


def test_parse_rm():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
