from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'dir D:\\Program Files\\',
        'expected': 'ls "/d/Program Files/"'
    },
    {
        'input': 'dir "D:\\Program Files\\"',
        'expected': 'ls "/d/Program Files/"'
    },
]


def test_parse_dir():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
