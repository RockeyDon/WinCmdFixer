from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'cp -r "D:\\Program Files\\" "C:\\Program Files"',
        'expected': 'robocopy /e "D:\\Program Files\\" "C:\\Program Files"'
    },
    {
        'input': 'cp "D:\\Program Files\\file.txt" C:\\Program Files',
        'expected': 'copy "D:\\Program Files\\file.txt" "C:\\Program Files"'
    },
]


def test_parse_cp():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
