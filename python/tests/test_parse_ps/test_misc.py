from src.win_cmd_fixer import fix_powershell

test_cases = [
    # echo -> Write-Output
    {
        'input': 'echo hello world',
        'expected': 'Write-Output hello world'
    },
    # echo with && -> ;
    {
        'input': 'echo hello && echo world',
        'expected': 'Write-Output hello ; Write-Output world'
    },
    # cls -> Clear-Host
    {
        'input': 'cls',
        'expected': 'Clear-Host'
    },
    # clear -> Clear-Host
    {
        'input': 'clear',
        'expected': 'Clear-Host'
    },
    # rename -> Rename-Item
    {
        'input': 'rename D:\\Program Files\\old.txt new.txt',
        'expected': 'Rename-Item "D:\\Program Files\\old.txt" new.txt'
    },
    # ren alias
    {
        'input': 'ren D:\\Program Files\\old.txt new.txt',
        'expected': 'Rename-Item "D:\\Program Files\\old.txt" new.txt'
    },
    # more -> Get-Content | Out-Host -Paging
    {
        'input': 'more D:\\Program Files\\file.txt',
        'expected': 'Get-Content "D:\\Program Files\\file.txt" | Out-Host -Paging'
    },
    # xcopy -> Copy-Item -Recurse
    {
        'input': 'xcopy D:\\Program Files\\src D:\\Program Files\\dst',
        'expected': 'Copy-Item "D:\\Program Files\\src" "D:\\Program Files\\dst" -Recurse'
    },
    # pushd -> Push-Location
    {
        'input': 'pushd D:\\Program Files\\',
        'expected': 'Push-Location "D:\\Program Files\\"'
    },
    # popd -> Pop-Location
    {
        'input': 'popd',
        'expected': 'Pop-Location'
    },
    # where -> Get-Command
    {
        'input': 'where python',
        'expected': 'Get-Command python'
    },
    # which -> Get-Command
    {
        'input': 'which python',
        'expected': 'Get-Command python'
    },
    # find -> Select-String
    {
        'input': 'find "hello" D:\\Program Files\\file.txt',
        'expected': 'Select-String "hello" "D:\\Program Files\\file.txt"'
    },
    # findstr -> Select-String
    {
        'input': 'findstr "pattern" D:\\Program Files\\file.txt',
        'expected': 'Select-String "pattern" "D:\\Program Files\\file.txt"'
    },
    # grep -> Select-String
    {
        'input': 'grep "pattern" D:\\Program Files\\file.txt',
        'expected': 'Select-String "pattern" "D:\\Program Files\\file.txt"'
    },
]


def test_parse_misc():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_powershell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
