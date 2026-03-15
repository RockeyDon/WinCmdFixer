from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'popd',
        'expected': 'popd'
    },
    # with trailing command
    {
        'input': 'popd && dir D:\\Program Files\\',
        'expected': 'popd && dir "D:\\Program Files\\"'
    },
]


def test_parse_popd():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
