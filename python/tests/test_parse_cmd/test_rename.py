from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'rename D:\\Program Files\\old.txt new.txt',
        'expected': 'ren "D:\\Program Files\\old.txt" new.txt'
    },
    {
        'input': 'rename "D:\\Program Files\\old.txt" new.txt',
        'expected': 'ren "D:\\Program Files\\old.txt" new.txt'
    },
    {
        'input': 'RENAME "D:\\Program Files\\old.txt" new.txt',
        'expected': 'ren "D:\\Program Files\\old.txt" new.txt'
    },
    # ren alias
    {
        'input': 'ren D:\\Program Files\\old.txt new.txt',
        'expected': 'ren "D:\\Program Files\\old.txt" new.txt'
    },
]


def test_parse_rename():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
