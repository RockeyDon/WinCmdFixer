import { fixCmd, fixPowershell, fixUnixShell } from '../src';

type Case = [string, string];

// ---------------------------------------------------------------
// 1. Already-correct commands should pass through unchanged
// ---------------------------------------------------------------

const correctCmdCases: Case[] = [
  ['cd /d "D:\\Program Files\\"', 'cd /d "D:\\Program Files\\"'],
  ['dir "D:\\Program Files\\"', 'dir "D:\\Program Files\\"'],
  ['copy "D:\\a.txt" "C:\\b.txt"', 'copy "D:\\a.txt" "C:\\b.txt"'],
  ['del "D:\\Program Files\\a.txt"', 'del "D:\\Program Files\\a.txt"'],
  ['move "D:\\a.txt" "C:\\b.txt"', 'move "D:\\a.txt" "C:\\b.txt"'],
  ['type "D:\\Program Files\\a.txt"', 'type "D:\\Program Files\\a.txt"'],
  ['mkdir "D:\\Program Files\\New"', 'mkdir "D:\\Program Files\\New"'],
  ['rmdir /S /Q "D:\\Program Files\\Old"', 'rmdir /S /Q "D:\\Program Files\\Old"'],
  ['ren "D:\\Program Files\\old.txt" new.txt', 'ren "D:\\Program Files\\old.txt" new.txt'],
  ['echo hello world', 'echo hello world'],
  ['cls', 'cls'],
  ['popd', 'popd'],
  ['where python', 'where python'],
  ['pushd "D:\\Program Files\\"', 'pushd "D:\\Program Files\\"'],
  ['find "hello" "D:\\a.txt"', 'find "hello" "D:\\a.txt"'],
  ['findstr /R "pattern" "D:\\a.txt"', 'findstr /R "pattern" "D:\\a.txt"'],
  ['more "D:\\Program Files\\a.txt"', 'more "D:\\Program Files\\a.txt"'],
  ['xcopy /S "D:\\a" "D:\\b"', 'xcopy /S "D:\\a" "D:\\b"'],
];

const correctPsCases: Case[] = [
  ['Set-Location "D:\\Program Files\\"', 'Set-Location "D:\\Program Files\\"'],
  ['Get-ChildItem "D:\\Program Files\\"', 'Get-ChildItem "D:\\Program Files\\"'],
  ['Copy-Item "D:\\a.txt" "C:\\b.txt"', 'Copy-Item "D:\\a.txt" "C:\\b.txt"'],
  ['Remove-Item "D:\\a.txt"', 'Remove-Item "D:\\a.txt"'],
  ['Move-Item "D:\\a.txt" "C:\\b.txt"', 'Move-Item "D:\\a.txt" "C:\\b.txt"'],
  ['Get-Content "D:\\a.txt"', 'Get-Content "D:\\a.txt"'],
  ['Clear-Host', 'Clear-Host'],
  ['Pop-Location', 'Pop-Location'],
  ['Get-Command python', 'Get-Command python'],
  ['Write-Output hello', 'Write-Output hello'],
];

describe('correct commands pass through unchanged', () => {
  describe('CMD', () => {
    test.each(correctCmdCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e));
  });
  describe('PowerShell', () => {
    test.each(correctPsCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e));
  });
});

// ---------------------------------------------------------------
// 2. Empty / whitespace / no-arg commands: never crash
// ---------------------------------------------------------------

const noCrashCmd: Case[] = [
  ['', ''],
  ['   ', ''],
  ['cd', 'cd'],
  ['cd ', 'cd'],
  ['dir', 'dir'],
  ['dir ', 'dir'],
  ['del', 'del'],
  ['copy', 'copy'],
  ['move', 'move'],
  ['type', 'type'],
  ['cls', 'cls'],
  ['cls ', 'cls'],
  ['popd', 'popd'],
  ['popd ', 'popd'],
  ['mkdir', 'mkdir'],
  ['rmdir', 'rmdir'],
  ['echo', 'echo'],
  ['more', 'more'],
  ['pushd', 'pushd'],
  ['where', 'where'],
  ['find', 'find'],
  ['findstr', 'findstr'],
  ['xcopy', 'xcopy'],
  ['rename', 'ren'],
  ['ren', 'ren'],
];

const noCrashPs: Case[] = [
  ['', ''],
  ['   ', ''],
  ['cd', 'Set-Location'],
  ['dir', 'Get-ChildItem'],
  ['del', 'Remove-Item'],
  ['copy', 'Copy-Item'],
  ['move', 'Move-Item'],
  ['type', 'Get-Content'],
  ['cls', 'Clear-Host'],
  ['popd', 'Pop-Location'],
  ['mkdir', 'New-Item -ItemType Directory -Path'],
  ['echo', 'Write-Output'],
  ['pushd', 'Push-Location'],
  ['where', 'Get-Command'],
];

const noCrashUnix: Case[] = [
  ['', ''],
  ['   ', ''],
  ['cd', 'cd'],
  ['dir', 'ls'],
  ['del', 'rm'],
  ['copy', 'cp'],
  ['move', 'mv'],
  ['type', 'cat'],
  ['cls', 'clear'],
  ['popd', 'popd'],
];

describe('no crash on empty / no-arg commands', () => {
  describe('CMD', () => {
    test.each(noCrashCmd)('fixCmd(%j)', (i, e) => expect(fixCmd(i)).toBe(e));
  });
  describe('PowerShell', () => {
    test.each(noCrashPs)('fixPowershell(%j)', (i, e) => expect(fixPowershell(i)).toBe(e));
  });
  describe('Unix', () => {
    test.each(noCrashUnix)('fixUnixShell(%j)', (i, e) => expect(fixUnixShell(i)).toBe(e));
  });
});

// ---------------------------------------------------------------
// 3. Unknown commands: pass through unchanged
// ---------------------------------------------------------------

const unknownCases: Case[] = [
  ['someunknown arg1 arg2', 'someunknown arg1 arg2'],
  ['notacmd', 'notacmd'],
  ['foo bar baz', 'foo bar baz'],
];

describe('unknown commands pass through', () => {
  test.each(unknownCases)('fixCmd(%j)', (i, e) => expect(fixCmd(i)).toBe(e));
});

// ---------------------------------------------------------------
// 4. Unknown command before separator, known command after
// ---------------------------------------------------------------

const skipSepCases: Case[] = [
  ['echo hello && cd D:\\Program Files\\', 'echo hello && cd /d "D:\\Program Files\\"'],
  ['echo hello && type D:\\Program Files\\file.txt', 'echo hello && type "D:\\Program Files\\file.txt"'],
  ['echo hello && echo world && dir D:\\Program Files\\', 'echo hello && echo world && dir "D:\\Program Files\\"'],
  ['foo bar | dir D:\\Program Files\\', 'foo bar | dir "D:\\Program Files\\"'],
];

describe('skip unknown command to separator', () => {
  test.each(skipSepCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e));
});

// ---------------------------------------------------------------
// 5. cd /D case-insensitive
// ---------------------------------------------------------------

const cdFlagCases: Case[] = [
  ['cd /D D:\\Program Files\\', 'cd /d "D:\\Program Files\\"'],
  ['cd /d D:\\Program Files\\', 'cd /d "D:\\Program Files\\"'],
];

describe('cd /D case-insensitive', () => {
  test.each(cdFlagCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e));
});
