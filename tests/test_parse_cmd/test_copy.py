from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'copy D:\\Program Files\\file.txt C:\\Program Files',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"'
    },
    {
        'input': 'copy "D:\\Program Files\\file.txt" C:\\Program Files',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"'
    },
    {
        'input': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"'
    },
    {
        'input': 'copy D:\\Program Files\\file.txt "C:\\Program Files"',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"'
    },
    {
        'input': 'COPY "D:\\Program Files\\file.txt" "C:\\Program Files"',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"'
    },
    # multi file
    {
        'input': 'copy D:\\Program Files\\file.txt C:\\Program Files\\file.txt "E:\\Program Files"',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt" "E:\\Program Files"'
    },
    # options
    {
        'input': 'copy /A D:\\Program Files\\file.txt /A C:\\Program Files\\file.txt /A "E:\\Program Files" /A',
        'expected': 'copy /A "D:\\Program Files\\file.txt" /A "C:\\Program Files\\file.txt" /A "E:\\Program Files" /A'
    },
    # concat
    {
        'input': 'copy D:\\Program Files\\file.txt + C:\\Program Files\\file.txt "E:\\Program Files"',
        'expected': 'copy "D:\\Program Files\\file.txt" + "C:\\Program Files\\file.txt" "E:\\Program Files"'
    },
]


def test_parse_copy():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
