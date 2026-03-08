from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'del D:\\Program Files\\file.txt',
        'expected': 'rm "/d/Program Files/file.txt"'
    },
    {
        'input': 'del "D:\\Program Files\\file.txt"',
        'expected': 'rm "/d/Program Files/file.txt"'
    },
    {
        'input': 'DEL "D:\\Program Files\\file.txt"',
        'expected': 'rm "/d/Program Files/file.txt"'
    },
    # multi file
    {
        'input': 'del D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'rm "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    {
        'input': 'del "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'rm "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    # options
    {
        'input': 'del -f "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'rm -f "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
]


def test_parse_del():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
