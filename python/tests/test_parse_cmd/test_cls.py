from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'cls',
        'expected': 'cls'
    },
    # clear alias
    {
        'input': 'clear',
        'expected': 'cls'
    },
    # with trailing separator
    {
        'input': 'cls && dir D:\\Program Files\\',
        'expected': 'cls && dir "D:\\Program Files\\"'
    },
    {
        'input': 'clear && dir D:\\Program Files\\',
        'expected': 'cls && dir "D:\\Program Files\\"'
    },
]


def test_parse_cls():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
