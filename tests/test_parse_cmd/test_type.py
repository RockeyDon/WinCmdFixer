from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'type D:\\Program Files\\file.txt',
        'expected': 'type "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'type "D:\\Program Files\\file.txt"',
        'expected': 'type "D:\\Program Files\\file.txt"'
    },
    {
        'input': 'TYPE "D:\\Program Files\\file.txt"',
        'expected': 'type "D:\\Program Files\\file.txt"'
    },
    # multi file
    {
        'input': 'type D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'type "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'type "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'type "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'
    },
    # combine
    {
        'input': 'type D:\\Program Files\\file.txt & type C:\\Program Files\\file.txt',
        'expected': 'type "D:\\Program Files\\file.txt" & type "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'type D:\\Program Files\\file.txt && type C:\\Program Files\\file.txt',
        'expected': 'type "D:\\Program Files\\file.txt" && type "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'type D:\\Program Files\\file.txt || type C:\\Program Files\\file.txt',
        'expected': 'type "D:\\Program Files\\file.txt" || type "C:\\Program Files\\file.txt"'
    },
    {
        'input': 'type D:\\Program Files\\file.txt > results.txt',
        'expected': 'type "D:\\Program Files\\file.txt" > results.txt'
    },
    {
        'input': 'type D:\\Program Files\\file.txt >> results.txt',
        'expected': 'type "D:\\Program Files\\file.txt" >> results.txt'
    },
    {
        'input': 'type D:\\Program Files\\file.txt | type C:\\Program Files\\file.txt > results.txt',
        'expected': 'type "D:\\Program Files\\file.txt" | type "C:\\Program Files\\file.txt" > results.txt'
    },
]


def test_parse_type():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
