from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'cd D:\\Program Files\\',
        'expected': 'cd "/d/Program Files/"'
    },
    {
        'input': 'cd "D:\\Program Files\\"',
        'expected': 'cd "/d/Program Files/"'
    },
    {
        'input': 'CD "D:\\Program Files\\"',
        'expected': 'cd "/d/Program Files/"'
    },
    # pre options
    {
        'input': 'cd D:\\Program Files\\',
        'expected': 'cd "/d/Program Files/"'
    },
    {
        'input': 'cd "D:\\Program Files\\"',
        'expected': 'cd "/d/Program Files/"'
    },
    # post options
    # combine
    {
        'input': 'cd D:\\Program Files\\ & cd C:\\Program Files\\',
        'expected': 'cd "/d/Program Files/" & cd "/c/Program Files/"'
    },
    {
        'input': 'cd D:\\Program Files\\ && cd C:\\Program Files\\',
        'expected': 'cd "/d/Program Files/" && cd "/c/Program Files/"'
    },
    {
        'input': 'cd D:\\Program Files\\ || cd C:\\Program Files\\',
        'expected': 'cd "/d/Program Files/" || cd "/c/Program Files/"'
    },
    {
        'input': 'cd D:\\Program Files\\ > results.txt',
        'expected': 'cd "/d/Program Files/" > results.txt'
    },
    {
        'input': 'cd D:\\Program Files\\ >> results.txt',
        'expected': 'cd "/d/Program Files/" >> results.txt'
    },
    {
        'input': 'cd D:\\Program Files\\ | cd C:\\Program Files\\ > results.txt',
        'expected': 'cd "/d/Program Files/" | cd "/c/Program Files/" > results.txt'
    },
]


def test_parse_cd():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
