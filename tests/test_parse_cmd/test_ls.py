from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'ls D:\\Program Files\\',
        'expected': 'dir "D:\\Program Files\\"'
    },
    {
        'input': 'ls "D:\\Program Files\\"',
        'expected': 'dir "D:\\Program Files\\"'
    },
]


def test_parse_ls():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
