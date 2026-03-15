from src.win_cmd_fixer import fix_powershell

test_cases = [
    # copy -> Copy-Item
    {
        'input': 'copy D:\\Program Files\\file.txt C:\\Program Files\\',
        'expected': 'Copy-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\"'
    },
    # cp -> Copy-Item
    {
        'input': 'cp D:\\Program Files\\file.txt C:\\Program Files\\',
        'expected': 'Copy-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\"'
    },
    # cp -r -> Copy-Item -Recurse
    {
        'input': 'cp -r D:\\Program Files\\src C:\\Program Files\\dst',
        'expected': 'Copy-Item "D:\\Program Files\\src" "C:\\Program Files\\dst" -Recurse'
    },
]


def test_parse_copy():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
