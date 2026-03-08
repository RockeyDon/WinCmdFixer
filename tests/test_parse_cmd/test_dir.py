from src.win_cmd_fixer import fix_cmd

test_cases = [
    # basic
    {
        'input': 'dir D:\\Program Files\\',
        'expected': 'dir "D:\\Program Files\\"'
    },
    {
        'input': 'dir "D:\\Program Files\\"',
        'expected': 'dir "D:\\Program Files\\"'
    },
    {
        'input': 'DIR "D:\\Program Files\\"',
        'expected': 'dir "D:\\Program Files\\"'
    },
    # pre options
    {
        'input': 'dir /P D:\\Program Files\\',
        'expected': 'dir /P "D:\\Program Files\\"'
    },
    {
        'input': 'dir /W "D:\\Program Files\\"',
        'expected': 'dir /W "D:\\Program Files\\"'
    },
    # post options
    {
        'input': 'dir D:\\Program Files\\ /P',
        'expected': 'dir "D:\\Program Files\\" /P'
    },
    {
        'input': 'dir "D:\\Program Files\\" /W',
        'expected': 'dir "D:\\Program Files\\" /W'
    },
    # combine
    {
        'input': 'dir D:\\Program Files\\ & dir C:\\Program Files\\',
        'expected': 'dir "D:\\Program Files\\" & dir "C:\\Program Files\\"'
    },
    {
        'input': 'dir D:\\Program Files\\ && dir C:\\Program Files\\',
        'expected': 'dir "D:\\Program Files\\" && dir "C:\\Program Files\\"'
    },
    {
        'input': 'dir D:\\Program Files\\ || dir C:\\Program Files\\',
        'expected': 'dir "D:\\Program Files\\" || dir "C:\\Program Files\\"'
    },
    {
        'input': 'dir D:\\Program Files\\ > results.txt',
        'expected': 'dir "D:\\Program Files\\" > results.txt'
    },
    {
        'input': 'dir D:\\Program Files\\ >> results.txt',
        'expected': 'dir "D:\\Program Files\\" >> results.txt'
    },
    {
        'input': 'dir D:\\Program Files\\ | dir C:\\Program Files\\ > results.txt',
        'expected': 'dir "D:\\Program Files\\" | dir "C:\\Program Files\\" > results.txt'
    },
]


def test_parse_dir():
    for ind, case in enumerate(test_cases, start=1):
        result = fix_cmd(case['input'])
        expected = case.get('expected_advanced', case.get('expected', []))
        assert result == expected
        print(f"✅ {ind}/{len(test_cases)}: {case['input']}")
