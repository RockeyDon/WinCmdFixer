from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'del D:\\Program Files\\file.txt',
        'expected': 'del "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'del "D:\\Program Files\\file.txt"',
        'expected': 'del "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'DEL "D:\\Program Files\\file.txt"',
        'expected': 'del "D:\\Program Files\\file.txt"'
    },
    # multi file
    {
        'input': 'del D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'del "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'del "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'del "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    # options
    {
        'input': 'del /P "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'del /P "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
]


def test_parse_del():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
