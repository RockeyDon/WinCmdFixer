from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'move D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'move "D:\\Program Files\\file.txt" C:\\Program Files\\file.txt',
        'expected': 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'move D:\\Program Files\\file.txt "C:\\Program Files\\file.txt"',
        'expected': 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'MOVE "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    # options
    {
        'input': 'move /Y D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'move /Y "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'move /-Y D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'move /-Y "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
]


def test_parse_move():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
