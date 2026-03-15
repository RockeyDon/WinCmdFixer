from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'find "hello" D:\\Program Files\\file.txt',
        'expected': 'find "hello" "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'find "hello" "D:\\Program Files\\file.txt"',
        'expected': 'find "hello" "D:\\Program Files\\file.txt"'
    },
    # with option
    {
        'input': 'find /I "hello" D:\\Program Files\\file.txt',
        'expected': 'find /I "hello" "D:\\Program Files\\file.txt"'
    },
]


def test_parse_find():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
