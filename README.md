# win-cmd-fixer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![npm version](https://img.shields.io/npm/v/win-cmd-fixer.svg)](https://www.npmjs.com/package/win-cmd-fixer)

**Convert problematic shell commands into Windows-compatible ones.**

Have you ever used a deep-agent, or pasted an AI-generated command, then got errors like "cannot find the path" or "syntax is incorrect"?

That command made perfect sense — but Windows CMD just wouldn't cooperate.

Then this tool is for you.

## Features

- Fix unquoted paths with spaces (e.g. `dir C:\Program Files` &rarr; `dir "C:\Program Files"`)
- Auto-add `/d` flag for cross-drive `cd`
- Translate Unix command names to their Windows equivalents (`cp` &rarr; `copy`, `ls` &rarr; `dir`, etc.)
- **Three output targets**: Windows CMD, PowerShell 5.x, and Unix shell
- Handles chained commands with `&&`, `||`, `|`, `>`, `>>` separators
- Supports 20+ commands: `cd`, `dir`, `copy`, `move`, `del`, `type`, `mkdir`, `rmdir`, `rename`, `echo`, `find`, `findstr`, `cls`, `more`, `xcopy`, `pushd`, `popd`, `where`, and their Unix aliases
- Already-correct commands pass through unchanged
- Unknown commands are emitted verbatim (never crashes)
- Zero dependencies — both the Python and TypeScript packages are fully standalone
- Available in both **Python** and **TypeScript**

## Installation

**Python**

```bash
pip install win-cmd-fixer
```

**TypeScript / JavaScript**

```bash
npm install win-cmd-fixer
```

## Usage

### Python

```python
from win_cmd_fixer import fix_cmd, fix_powershell, fix_unix_shell

# Fix for Windows CMD
fix_cmd('cd D:\\Program Files\\project')
# => 'cd /d "D:\\Program Files\\project"'

fix_cmd('cp -r D:\\Program Files\\src C:\\Program Files\\dst')
# => 'robocopy /e "D:\\Program Files\\src" "C:\\Program Files\\dst"'

# Fix for PowerShell 5.x
fix_powershell('cd D:\\Program Files\\project')
# => 'Set-Location "D:\\Program Files\\project"'

fix_powershell('rm -rf D:\\Program Files\\old')
# => 'Remove-Item "D:\\Program Files\\old" -Recurse -Force'

# Fix for Unix shell (e.g. Git Bash, WSL)
fix_unix_shell('dir D:\\Program Files\\')
# => 'ls "/d/Program Files/"'
```

### TypeScript / JavaScript

```typescript
import {fixCmd, fixPowershell, fixUnixShell} from 'win-cmd-fixer';

// Fix for Windows CMD
fixCmd('cd D:\\Program Files\\project');
// => 'cd /d "D:\\Program Files\\project"'

fixCmd('cp -r D:\\Program Files\\src C:\\Program Files\\dst');
// => 'robocopy /e "D:\\Program Files\\src" "C:\\Program Files\\dst"'

// Fix for PowerShell 5.x
fixPowershell('cd D:\\Program Files\\project');
// => 'Set-Location "D:\\Program Files\\project"'

// Fix for Unix shell
fixUnixShell('dir D:\\Program Files\\');
// => 'ls "/d/Program Files/"'
```

## What It Fixes

| Issue              | Example                 | CMD                       | PowerShell                                 | Unix                     |
|--------------------|-------------------------|---------------------------|--------------------------------------------|--------------------------|
| Paths with spaces  | `dir C:\Program Files`  | `dir "C:\Program Files"`  | `Get-ChildItem "C:\Program Files"`         | `ls "/c/Program Files"`  |
| Cross-drive `cd`   | `cd D:\folder`          | `cd /d "D:\folder"`       | `Set-Location "D:\folder"`                 | `cd "/d/folder"`         |
| Unix command names | `cp file.txt dest\`     | `copy file.txt dest\`     | `Copy-Item file.txt dest\`                 | `cp file.txt dest/`      |
| `rm -rf`           | `rm -rf D:\old`         | `rmdir /s /q "D:\old"`    | `Remove-Item "D:\old" -Recurse -Force`     | `rm -rf "/d/old"`        |
| `cp -r`            | `cp -r src dst`         | `robocopy /e src dst`     | `Copy-Item src dst -Recurse`               | `cp -r src dst`          |
| `grep`             | `grep "pat" file`       | `findstr "pat" file`      | `Select-String "pat" file`                 | `grep "pat" file`        |
| `clear`            | `clear`                 | `cls`                     | `Clear-Host`                               | `clear`                  |
| `which`            | `which python`          | `where python`            | `Get-Command python`                       | `which python`           |
| Chained commands   | `echo hi && dir C:\P F` | `echo hi && dir "C:\P F"` | `Write-Output hi ; Get-ChildItem "C:\P F"` | `echo hi && ls "/c/P F"` |

## API Reference

### Python

| Function                           | Description                            |
|------------------------------------|----------------------------------------|
| `fix_cmd(text: str) -> str`        | Convert to valid Windows CMD syntax    |
| `fix_powershell(text: str) -> str` | Convert to valid PowerShell 5.x syntax |
| `fix_unix_shell(text: str) -> str` | Convert to valid Unix shell syntax     |

### TypeScript

| Function                              | Description                            |
|---------------------------------------|----------------------------------------|
| `fixCmd(text: string): string`        | Convert to valid Windows CMD syntax    |
| `fixPowershell(text: string): string` | Convert to valid PowerShell 5.x syntax |
| `fixUnixShell(text: string): string`  | Convert to valid Unix shell syntax     |

## Contributing

Contributions are welcome! Especially:

- New edge cases you've encountered
- Better heuristics for path detection
- Support for more commands or shell variations

### Setup

```bash
git clone https://github.com/RockeyDon/win-cmd-fixer.git
cd win-cmd-fixer
```

**Python**

```bash
cd python
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -e ".[dev]"
pytest tests/
```

**TypeScript**

```bash
cd typescript
npm install
npm test
```

### Build & Publish

A single PowerShell script handles both packages:

```powershell
# Build only (dry run)
.\publish.ps1

# Build and publish to PyPI + npm
.\publish.ps1 -Publish

# Publish Python to TestPyPI, npm dry-run
.\publish.ps1 -Publish -TestPyPI
```

## License

[MIT](LICENSE)
