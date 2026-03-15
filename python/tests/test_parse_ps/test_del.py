from src.win_cmd_fixer import fix_powershell

test_cases = [
    # del -> Remove-Item
    {
        'input': 'del D:\\Program Files\\file.txt',
        'expected': 'Remove-Item "D:\\Program Files\\file.txt"'
    },
    # rm -> Remove-Item
    {
        'input': 'rm D:\\Program Files\\file.txt',
        'expected': 'Remove-Item "D:\\Program Files\\file.txt"'
    },
    # rm -rf -> Remove-Item -Recurse -Force
    {
        'input': 'rm -rf D:\\Program Files\\OldFolder',
        'expected': 'Remove-Item "D:\\Program Files\\OldFolder" -Recurse -Force'
    },
    # rm -r -> Remove-Item -Recurse
    {
        'input': 'rm -r D:\\Program Files\\OldFolder',
        'expected': 'Remove-Item "D:\\Program Files\\OldFolder" -Recurse'
    },
]


def test_parse_del():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
