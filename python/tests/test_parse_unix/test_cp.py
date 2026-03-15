from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # basic
    {
        'input': 'cp D:\\Program Files\\file.txt C:\\Program Files',
        'expected': 'cp "/d/Program Files/file.txt" "/c/Program Files"'
    },
    {
        'input': 'cp "D:\\Program Files\\file.txt" C:\\Program Files',
        'expected': 'cp "/d/Program Files/file.txt" "/c/Program Files"'
    },
    {
        'input': 'cp "D:\\Program Files\\file.txt" "C:\\Program Files"',
        'expected': 'cp "/d/Program Files/file.txt" "/c/Program Files"'
    },
    {
        'input': 'cp D:\\Program Files\\file.txt "C:\\Program Files"',
        'expected': 'cp "/d/Program Files/file.txt" "/c/Program Files"'
    },
    {
        'input': 'COPY "D:\\Program Files\\file.txt" "C:\\Program Files"',
        'expected': 'cp "/d/Program Files/file.txt" "/c/Program Files"'
    },
    # multi file
    {
        'input': 'cp D:\\Program Files\\file.txt C:\\Program Files\\file.txt "E:\\Program Files"',
        'expected': 'cp "/d/Program Files/file.txt" "/c/Program Files/file.txt" "/e/Program Files"'
    },
    # options
    {
        'input': 'cp -r D:\\Program Files\\file.txt C:\\Program Files\\file.txt "E:\\Program Files"',
        'expected': 'cp -r "/d/Program Files/file.txt" "/c/Program Files/file.txt" "/e/Program Files"'
    },
    # concat
    {
        'input': 'cp D:\\Program Files\\file.txt + C:\\Program Files\\file.txt "E:\\Program Files"',
        'expected': 'cp "/d/Program Files/file.txt" + "/c/Program Files/file.txt" "/e/Program Files"'
    },
]


def test_parse_cp():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
