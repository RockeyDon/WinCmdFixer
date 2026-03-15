from src.win_cmd_fixer import fix_powershell

test_cases = [
    # mkdir -> New-Item -ItemType Directory
    {
        'input': 'mkdir D:\\Program Files\\NewFolder',
        'expected': 'New-Item -ItemType Directory -Path "D:\\Program Files\\NewFolder"'
    },
    # md alias
    {
        'input': 'md D:\\Program Files\\NewFolder',
        'expected': 'New-Item -ItemType Directory -Path "D:\\Program Files\\NewFolder"'
    },
    # rmdir -> Remove-Item
    {
        'input': 'rmdir D:\\Program Files\\OldFolder',
        'expected': 'Remove-Item "D:\\Program Files\\OldFolder"'
    },
    # rmdir /s /q -> Remove-Item -Recurse -Force
    {
        'input': 'rmdir /S /Q D:\\Program Files\\OldFolder',
        'expected': 'Remove-Item "D:\\Program Files\\OldFolder" -Recurse -Force'
    },
    # rd alias
    {
        'input': 'rd D:\\Program Files\\OldFolder',
        'expected': 'Remove-Item "D:\\Program Files\\OldFolder"'
    },
]


def test_parse_mkdir_rmdir():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
