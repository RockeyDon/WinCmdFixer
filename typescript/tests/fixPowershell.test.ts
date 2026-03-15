import { fixPowershell } from '../src';

type Case = [string, string];

const cdCases: Case[] = [
  ['cd D:\\Program Files\\', 'Set-Location "D:\\Program Files\\"'],
  ['cd "D:\\Program Files\\"', 'Set-Location "D:\\Program Files\\"'],
  ['CD "D:\\Program Files\\"', 'Set-Location "D:\\Program Files\\"'],
  ['cd /d D:\\Program Files\\', 'Set-Location "D:\\Program Files\\"'],
  ['cd /D D:\\Program Files\\', 'Set-Location "D:\\Program Files\\"'],
  ['cd D:\\Program Files\\ && cd C:\\Program Files\\', 'Set-Location "D:\\Program Files\\" ; Set-Location "C:\\Program Files\\"'],
  ['cd D:\\Program Files\\ || cd C:\\Program Files\\', 'Set-Location "D:\\Program Files\\" ; Set-Location "C:\\Program Files\\"'],
  ['cd D:\\Program Files\\ | cd C:\\Program Files\\', 'Set-Location "D:\\Program Files\\" | Set-Location "C:\\Program Files\\"'],
  ['cd D:\\Program Files\\ > results.txt', 'Set-Location "D:\\Program Files\\" > results.txt'],
];

const dirCases: Case[] = [
  ['dir D:\\Program Files\\', 'Get-ChildItem "D:\\Program Files\\"'],
  ['dir "D:\\Program Files\\"', 'Get-ChildItem "D:\\Program Files\\"'],
  ['ls D:\\Program Files\\', 'Get-ChildItem "D:\\Program Files\\"'],
  ['dir D:\\Program Files\\ && dir C:\\Program Files\\', 'Get-ChildItem "D:\\Program Files\\" ; Get-ChildItem "C:\\Program Files\\"'],
];

const copyCases: Case[] = [
  ['copy D:\\Program Files\\file.txt C:\\Program Files\\', 'Copy-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['cp D:\\Program Files\\file.txt C:\\Program Files\\', 'Copy-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['cp -r D:\\Program Files\\src C:\\Program Files\\dst', 'Copy-Item "D:\\Program Files\\src" "C:\\Program Files\\dst" -Recurse'],
];

const moveCases: Case[] = [
  ['move D:\\Program Files\\file.txt C:\\Program Files\\file.txt', 'Move-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
  ['mv D:\\Program Files\\file.txt C:\\Program Files\\file.txt', 'Move-Item "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
  ['move D:\\a.txt C:\\b.txt && move D:\\c.txt C:\\d.txt', 'Move-Item "D:\\a.txt" "C:\\b.txt" ; Move-Item "D:\\c.txt" "C:\\d.txt"'],
];

const delCases: Case[] = [
  ['del D:\\Program Files\\file.txt', 'Remove-Item "D:\\Program Files\\file.txt"'],
  ['rm D:\\Program Files\\file.txt', 'Remove-Item "D:\\Program Files\\file.txt"'],
  ['rm -rf D:\\Program Files\\OldFolder', 'Remove-Item "D:\\Program Files\\OldFolder" -Recurse -Force'],
  ['rm -r D:\\Program Files\\OldFolder', 'Remove-Item "D:\\Program Files\\OldFolder" -Recurse'],
];

const typeCases: Case[] = [
  ['type D:\\Program Files\\file.txt', 'Get-Content "D:\\Program Files\\file.txt"'],
  ['cat D:\\Program Files\\file.txt', 'Get-Content "D:\\Program Files\\file.txt"'],
  ['type D:\\Program Files\\a.txt && type D:\\Program Files\\b.txt', 'Get-Content "D:\\Program Files\\a.txt" ; Get-Content "D:\\Program Files\\b.txt"'],
];

const mkdirCases: Case[] = [
  ['mkdir D:\\Program Files\\NewFolder', 'New-Item -ItemType Directory -Path "D:\\Program Files\\NewFolder"'],
  ['md D:\\Program Files\\NewFolder', 'New-Item -ItemType Directory -Path "D:\\Program Files\\NewFolder"'],
  ['rmdir D:\\Program Files\\OldFolder', 'Remove-Item "D:\\Program Files\\OldFolder"'],
  ['rmdir /S /Q D:\\Program Files\\OldFolder', 'Remove-Item "D:\\Program Files\\OldFolder" -Recurse -Force'],
  ['rd D:\\Program Files\\OldFolder', 'Remove-Item "D:\\Program Files\\OldFolder"'],
];

const miscCases: Case[] = [
  ['echo hello world', 'Write-Output hello world'],
  ['echo hello && echo world', 'Write-Output hello ; Write-Output world'],
  ['cls', 'Clear-Host'],
  ['clear', 'Clear-Host'],
  ['rename D:\\Program Files\\old.txt new.txt', 'Rename-Item "D:\\Program Files\\old.txt" new.txt'],
  ['ren D:\\Program Files\\old.txt new.txt', 'Rename-Item "D:\\Program Files\\old.txt" new.txt'],
  ['more D:\\Program Files\\file.txt', 'Get-Content "D:\\Program Files\\file.txt" | Out-Host -Paging'],
  ['xcopy D:\\Program Files\\src D:\\Program Files\\dst', 'Copy-Item "D:\\Program Files\\src" "D:\\Program Files\\dst" -Recurse'],
  ['pushd D:\\Program Files\\', 'Push-Location "D:\\Program Files\\"'],
  ['popd', 'Pop-Location'],
  ['where python', 'Get-Command python'],
  ['which python', 'Get-Command python'],
  ['find "hello" D:\\Program Files\\file.txt', 'Select-String "hello" "D:\\Program Files\\file.txt"'],
  ['findstr "pattern" D:\\Program Files\\file.txt', 'Select-String "pattern" "D:\\Program Files\\file.txt"'],
  ['grep "pattern" D:\\Program Files\\file.txt', 'Select-String "pattern" "D:\\Program Files\\file.txt"'],
];

describe('fixPowershell', () => {
  describe('cd', () => { test.each(cdCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('dir', () => { test.each(dirCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('copy', () => { test.each(copyCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('move', () => { test.each(moveCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('del/rm', () => { test.each(delCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('type/cat', () => { test.each(typeCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('mkdir/rmdir', () => { test.each(mkdirCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
  describe('misc', () => { test.each(miscCases)('%s', (i, e) => expect(fixPowershell(i)).toBe(e)); });
});
