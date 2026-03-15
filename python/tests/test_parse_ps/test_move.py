from src.win_cmd_fixer import fix_powershell

test_cases = [
    # move -> Move-Item
    {
        'input': 'move D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'Move-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    # mv alias
    {
        'input': 'mv D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'Move-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    # && -> ;
    {
        'input': 'move D:\\a.txt C:\\b.txt && move D:\\c.txt C:\\d.txt',
        'expected': 'Move-Item "D:\\a.txt" "C:\\b.txt" ; Move-Item "D:\\c.txt" "C:\\d.txt"'
    },
]


def test_parse_move():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
