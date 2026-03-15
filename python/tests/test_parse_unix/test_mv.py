from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'mv D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    {
        'input': 'mv "D:\\Program Files\\file.txt" C:\\Program Files\\file.txt',
        'expected': 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    {
        'input': 'mv "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    {
        'input': 'mv D:\\Program Files\\file.txt "C:\\Program Files\\file.txt"',
        'expected': 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    {
        'input': 'MV "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    # options
    {
        'input': 'mv -r D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'mv -r "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
]


def test_parse_mv():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
