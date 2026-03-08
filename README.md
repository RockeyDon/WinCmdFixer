# win-cmd-fixer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)

**Convert problematic shell commands into Windows compatible ones.**

Have you ever use deep-agent, or paste AI-generated command, then got errors like "cannot find the path" or "syntax is incorrect"?

That command made perfect sense — but Windows CMD just wouldn't cooperate.

Then this tool is for you.

## Usage

```python
from win_cmd_fixer import fix_cmd

cmd = fix_cmd('cd D:\my projects')
```

## What it fixes

| Issue                 | Example                     | Fixed                         |
|-----------------------|-----------------------------|-------------------------------|
| **Paths with spaces** | dir C:\Program Files        | dir "C:\Program Files"        |
| **Cross-drive `cd`**  | cd D:\folder                | cd /d D:\folder               |
| **Unix-style name**   | cp D:\folder\file C:\folder | copy D:\folder\file C:\folder |

## Contributing

Contributions are welcome! Especially:

- New edge cases you've encountered
- Better heuristics for path detection
- Support for more Windows shell variations (PowerShell, pwsh, Git Bash)

### Setup

```bash
git clone https://github.com/RockeyDon/win-cmd-fixer.git
cd win-cmd-fixer
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
```
