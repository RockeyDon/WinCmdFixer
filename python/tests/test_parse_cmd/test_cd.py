from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'cd D:\\Program Files\\',
        'expected': 'cd /d "D:\\Program Files\\"'
    },
    {
        'input': 'cd "D:\\Program Files\\"',
        'expected': 'cd /d "D:\\Program Files\\"'
    },
    {
        'input': 'CD "D:\\Program Files\\"',
        'expected': 'cd /d "D:\\Program Files\\"'
    },
    # pre options
    {
        'input': 'cd /d D:\\Program Files\\',
        'expected': 'cd /d "D:\\Program Files\\"'
    },
    {
        'input': 'cd /d "D:\\Program Files\\"',
        'expected': 'cd /d "D:\\Program Files\\"'
    },
    # post options
    # combine
    {
        'input': 'cd D:\\Program Files\\ & cd C:\\Program Files\\',
        'expected': 'cd /d "D:\\Program Files\\" & cd /d "C:\\Program Files\\"'
    },
    {
        'input': 'cd /d D:\\Program Files\\ && cd /d C:\\Program Files\\',
        'expected': 'cd /d "D:\\Program Files\\" && cd /d "C:\\Program Files\\"'
    },
    {
        'input': 'cd /d D:\\Program Files\\ || cd /d C:\\Program Files\\',
        'expected': 'cd /d "D:\\Program Files\\" || cd /d "C:\\Program Files\\"'
    },
    {
        'input': 'cd /d D:\\Program Files\\ > results.txt',
        'expected': 'cd /d "D:\\Program Files\\" > results.txt'
    },
    {
        'input': 'cd /d D:\\Program Files\\ >> results.txt',
        'expected': 'cd /d "D:\\Program Files\\" >> results.txt'
    },
    {
        'input': 'cd /d D:\\Program Files\\ | cd /d C:\\Program Files\\ > results.txt',
        'expected': 'cd /d "D:\\Program Files\\" | cd /d "C:\\Program Files\\" > results.txt'
    },
]


def test_parse_cd():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
