from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'xcopy D:\\Program Files\\src D:\\Program Files\\dst',
        'expected': 'xcopy "D:\\Program Files\\src" "D:\\Program Files\\dst"'
    },
    {
        'input': 'xcopy "D:\\Program Files\\src" "D:\\Program Files\\dst"',
        'expected': 'xcopy "D:\\Program Files\\src" "D:\\Program Files\\dst"'
    },
    # with options
    {
        'input': 'xcopy /S /E D:\\Program Files\\src D:\\Program Files\\dst',
        'expected': 'xcopy /S /E "D:\\Program Files\\src" "D:\\Program Files\\dst"'
    },
]


def test_parse_xcopy():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
