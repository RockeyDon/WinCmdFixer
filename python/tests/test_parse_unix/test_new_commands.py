from src.win_cmd_fixer import fix_unix_shell

test_cases = [
    # mkdir
    {
        'input': 'mkdir D:\\Program Files\\NewFolder',
        'expected': 'mkdir "/d/Program Files/NewFolder"'
    },
    # rmdir
    {
        'input': 'rmdir D:\\Program Files\\OldFolder',
        'expected': 'rmdir "/d/Program Files/OldFolder"'
    },
    # rename -> mv
    {
        'input': 'rename D:\\Program Files\\old.txt new.txt',
        'expected': 'mv "/d/Program Files/old.txt" new.txt'
    },
    # echo
    {
        'input': 'echo hello world',
        'expected': 'echo hello world'
    },
    # cls -> clear
    {
        'input': 'cls',
        'expected': 'clear'
    },
    # clear stays clear
    {
        'input': 'clear',
        'expected': 'clear'
    },
    # more
    {
        'input': 'more D:\\Program Files\\file.txt',
        'expected': 'more "/d/Program Files/file.txt"'
    },
    # xcopy -> cp -r
    {
        'input': 'xcopy D:\\Program Files\\src D:\\Program Files\\dst',
        'expected': 'cp -r "/d/Program Files/src" "/d/Program Files/dst"'
    },
    # pushd
    {
        'input': 'pushd D:\\Program Files\\',
        'expected': 'pushd "/d/Program Files/"'
    },
    # popd
    {
        'input': 'popd',
        'expected': 'popd'
    },
    # where -> which
    {
        'input': 'where python',
        'expected': 'which python'
    },
    # which stays which
    {
        'input': 'which python',
        'expected': 'which python'
    },
    # find -> grep
    {
        'input': 'find "hello" D:\\Program Files\\file.txt',
        'expected': 'grep "hello" "/d/Program Files/file.txt"'
    },
    # findstr -> grep
    {
        'input': 'findstr "pattern" D:\\Program Files\\file.txt',
        'expected': 'grep "pattern" "/d/Program Files/file.txt"'
    },
    # grep stays grep
    {
        'input': 'grep "pattern" D:\\Program Files\\file.txt',
        'expected': 'grep "pattern" "/d/Program Files/file.txt"'
    },
    # rm -rf
    {
        'input': 'rm -rf D:\\Program Files\\OldFolder',
        'expected': 'rm -rf "/d/Program Files/OldFolder"'
    },
]


def test_parse_new_commands():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_unix_shell(case['input'])
        expected = case.get('expected', '')
        assert result == expected, f"Case {ind} failed: {case['input']!r} => {result!r}"
        print(f"PASS {ind}/{len(test_cases)}: {case['input']}")
