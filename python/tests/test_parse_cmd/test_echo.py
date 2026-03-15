from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'echo hello world',
        'expected': 'echo hello world'
    },
    # with separator
    {
        'input': 'echo hello && echo world',
        'expected': 'echo hello && echo world'
    },
    {
        'input': 'echo hello > output.txt',
        'expected': 'echo hello > output.txt'
    },
    {
        'input': 'echo hello >> output.txt',
        'expected': 'echo hello >> output.txt'
    },
    # pipe
    {
        'input': 'echo hello | find "h"',
        'expected': 'echo hello | find "h"'
    },
]


def test_parse_echo():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
