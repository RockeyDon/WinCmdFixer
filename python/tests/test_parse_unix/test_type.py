from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'type D:\\Program Files\\file.txt',
        'expected': 'cat "/d/Program Files/file.txt"'
    },
    {
        'input': 'type "D:\\Program Files\\file.txt"',
        'expected': 'cat "/d/Program Files/file.txt"'
    },
]


def test_parse_type():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
