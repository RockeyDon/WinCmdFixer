from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'findstr "pattern" D:\\Program Files\\file.txt',
        'expected': 'findstr "pattern" "D:\\Program Files\\file.txt"'
    },
    # with option
    {
        'input': 'findstr /R "pattern" D:\\Program Files\\file.txt',
        'expected': 'findstr /R "pattern" "D:\\Program Files\\file.txt"'
    },
    # grep alias
    {
        'input': 'grep "pattern" D:\\Program Files\\file.txt',
        'expected': 'findstr "pattern" "D:\\Program Files\\file.txt"'
    },
]


def test_parse_findstr():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
