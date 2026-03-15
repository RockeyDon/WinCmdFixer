from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'ls D:\\Program Files\\',
        'expected': 'ls "/d/Program Files/"'
    },
    {
        'input': 'ls "D:\\Program Files\\"',
        'expected': 'ls "/d/Program Files/"'
    },
    {
        'input': 'LS "D:\\Program Files\\"',
        'expected': 'ls "/d/Program Files/"'
    },
    # pre options
    {
        'input': 'ls -l D:\\Program Files\\',
        'expected': 'ls -l "/d/Program Files/"'
    },
    {
        'input': 'ls -lh "D:\\Program Files\\"',
        'expected': 'ls -lh "/d/Program Files/"'
    },
    # combine
    {
        'input': 'ls D:\\Program Files\\ & ls C:\\Program Files\\',
        'expected': 'ls "/d/Program Files/" & ls "/c/Program Files/"'
    },
    {
        'input': 'ls D:\\Program Files\\ && ls C:\\Program Files\\',
        'expected': 'ls "/d/Program Files/" && ls "/c/Program Files/"'
    },
    {
        'input': 'ls D:\\Program Files\\ || ls C:\\Program Files\\',
        'expected': 'ls "/d/Program Files/" || ls "/c/Program Files/"'
    },
    {
        'input': 'ls D:\\Program Files\\ > results.txt',
        'expected': 'ls "/d/Program Files/" > results.txt'
    },
    {
        'input': 'ls D:\\Program Files\\ >> results.txt',
        'expected': 'ls "/d/Program Files/" >> results.txt'
    },
    {
        'input': 'ls D:\\Program Files\\ | ls C:\\Program Files\\ > results.txt',
        'expected': 'ls "/d/Program Files/" | ls "/c/Program Files/" > results.txt'
    },
]


def test_parse_ls():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
