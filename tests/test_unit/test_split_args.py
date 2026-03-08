from src.win_cmd_fixer.args import split_args

test_cases = [
    # basic
    {
        'input': 'dir D:\\Program Files\\',
        'expected': ['dir', 'D:\\Program', 'Files\\']
    },
    {
        'input': 'dir "D:\\Program Files\\"',
        'expected': ['dir', 'D:\\Program Files\\']
    },
    # mixed quote
    {
        'input': "echo 'hello world' > file.txt",
        'expected': ['echo', 'hello world', '>', 'file.txt']
    },
    # many args
    {
        'input': 'copy "C:\\my files\\file1.txt" "D:\\backup files\\"',
        'expected': ['copy', 'C:\\my files\\file1.txt', 'D:\\backup files\\']
    },
    # space + quote
    {
        'input': 'program -o "value with spaces" --flag',
        'expected': ['program', '-o', 'value with spaces', '--flag']
    },
    # blank quote
    {
        'input': 'echo ""',
        'expected': ['echo', '']
    },
    # many space
    {
        'input': 'command    arg1    "arg2 with spaces"    arg3',
        'expected': ['command', 'arg1', 'arg2 with spaces', 'arg3']
    }
]


def test_split_functions():
    for ind, case in enumerate(test_cases, start=1):
        result = split_args(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected, f"Failed on {case['input']}"
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
