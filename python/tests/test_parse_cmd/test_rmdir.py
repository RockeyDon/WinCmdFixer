from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'rmdir D:\\Program Files\\OldFolder',
        'expected': 'rmdir "D:\\Program Files\\OldFolder"'
    },
    {
        'input': 'rmdir "D:\\Program Files\\OldFolder"',
        'expected': 'rmdir "D:\\Program Files\\OldFolder"'
    },
    {
        'input': 'RMDIR "D:\\Program Files\\OldFolder"',
        'expected': 'rmdir "D:\\Program Files\\OldFolder"'
    },
    # rd alias
    {
        'input': 'rd D:\\Program Files\\OldFolder',
        'expected': 'rmdir "D:\\Program Files\\OldFolder"'
    },
    # with options
    {
        'input': 'rmdir /S /Q D:\\Program Files\\OldFolder',
        'expected': 'rmdir /S /Q "D:\\Program Files\\OldFolder"'
    },
    # combine
    {
        'input': 'rmdir D:\\Program Files\\A && rmdir D:\\Program Files\\B',
        'expected': 'rmdir "D:\\Program Files\\A" && rmdir "D:\\Program Files\\B"'
    },
]


def test_parse_rmdir():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
