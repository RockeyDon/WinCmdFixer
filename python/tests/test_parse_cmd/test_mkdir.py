from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'mkdir D:\\Program Files\\NewFolder',
        'expected': 'mkdir "D:\\Program Files\\NewFolder"'
    },
    {
        'input': 'mkdir "D:\\Program Files\\NewFolder"',
        'expected': 'mkdir "D:\\Program Files\\NewFolder"'
    },
    {
        'input': 'MKDIR "D:\\Program Files\\NewFolder"',
        'expected': 'mkdir "D:\\Program Files\\NewFolder"'
    },
    # md alias
    {
        'input': 'md D:\\Program Files\\NewFolder',
        'expected': 'mkdir "D:\\Program Files\\NewFolder"'
    },
    # combine
    {
        'input': 'mkdir D:\\Program Files\\A && mkdir D:\\Program Files\\B',
        'expected': 'mkdir "D:\\Program Files\\A" && mkdir "D:\\Program Files\\B"'
    },
]


def test_parse_mkdir():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
