from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'cat D:\\Program Files\\file.txt',
        'expected': 'cat "/d/Program Files/file.txt"'
    },
    {
        'input': 'cat "D:\\Program Files\\file.txt"',
        'expected': 'cat "/d/Program Files/file.txt"'
    },
    {
        'input': 'CAT "D:\\Program Files\\file.txt"',
        'expected': 'cat "/d/Program Files/file.txt"'
    },
    # multi file
    {
        'input': 'cat D:\\Program Files\\file.txt C:\\Program Files\\file.txt',
        'expected': 'cat "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    {
        'input': 'cat "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"',
        'expected': 'cat "/d/Program Files/file.txt" "/c/Program Files/file.txt"'
    },
    # combine
    {
        'input': 'cat D:\\Program Files\\file.txt & cat C:\\Program Files\\file.txt',
        'expected': 'cat "/d/Program Files/file.txt" & cat "/c/Program Files/file.txt"'
    },
    {
        'input': 'cat D:\\Program Files\\file.txt && cat C:\\Program Files\\file.txt',
        'expected': 'cat "/d/Program Files/file.txt" && cat "/c/Program Files/file.txt"'
    },
    {
        'input': 'cat D:\\Program Files\\file.txt || cat C:\\Program Files\\file.txt',
        'expected': 'cat "/d/Program Files/file.txt" || cat "/c/Program Files/file.txt"'
    },
    {
        'input': 'cat D:\\Program Files\\file.txt > results.txt',
        'expected': 'cat "/d/Program Files/file.txt" > results.txt'
    },
    {
        'input': 'cat D:\\Program Files\\file.txt >> results.txt',
        'expected': 'cat "/d/Program Files/file.txt" >> results.txt'
    },
    {
        'input': 'cat D:\\Program Files\\file.txt | cat C:\\Program Files\\file.txt > results.txt',
        'expected': 'cat "/d/Program Files/file.txt" | cat "/c/Program Files/file.txt" > results.txt'
    },
]


def test_parse_cat():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
