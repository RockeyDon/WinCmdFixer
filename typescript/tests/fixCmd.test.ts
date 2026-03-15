import { fixCmd } from '../src';

// Each entry: [input, expected]
type Case = [string, string];

const cdCases: Case[] = [
  ['cd D:\\Program Files\\', 'cd /d "D:\\Program Files\\"'],
  ['cd "D:\\Program Files\\"', 'cd /d "D:\\Program Files\\"'],
  ['CD "D:\\Program Files\\"', 'cd /d "D:\\Program Files\\"'],
  ['cd /D D:\\Program Files\\', 'cd /d "D:\\Program Files\\"'],
  ['cd /d D:\\Program Files\\', 'cd /d "D:\\Program Files\\"'],
  ['cd D:\\Program Files\\ && cd C:\\Program Files\\', 'cd /d "D:\\Program Files\\" && cd /d "C:\\Program Files\\"'],
  ['cd D:\\NoSpace\\', 'cd /d "D:\\NoSpace\\"'],
  ['cd D:\\Program Files\\ > output.txt', 'cd /d "D:\\Program Files\\" > output.txt'],
];

const copyCases: Case[] = [
  ['copy D:\\Program Files\\file.txt C:\\Program Files\\', 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"', 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['COPY "D:\\Program Files\\file.txt" "C:\\Program Files\\"', 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
];

const cpCases: Case[] = [
  ['cp D:\\Program Files\\file.txt C:\\Program Files\\', 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['cp "D:\\Program Files\\file.txt" "C:\\Program Files\\"', 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['CP "D:\\Program Files\\file.txt" "C:\\Program Files\\"', 'copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"'],
  ['cp -r D:\\Program Files\\src C:\\Program Files\\dst', 'robocopy /e "D:\\Program Files\\src" "C:\\Program Files\\dst"'],
];

const delCases: Case[] = [
  ['del D:\\Program Files\\file.txt', 'del "D:\\Program Files\\file.txt"'],
  ['del "D:\\Program Files\\file.txt"', 'del "D:\\Program Files\\file.txt"'],
  ['DEL "D:\\Program Files\\file.txt"', 'del "D:\\Program Files\\file.txt"'],
  ['del /P D:\\Program Files\\file.txt', 'del /P "D:\\Program Files\\file.txt"'],
];

const dirCases: Case[] = [
  ['dir D:\\Program Files\\', 'dir "D:\\Program Files\\"'],
  ['dir "D:\\Program Files\\"', 'dir "D:\\Program Files\\"'],
  ['DIR "D:\\Program Files\\"', 'dir "D:\\Program Files\\"'],
  ['dir /P D:\\Program Files\\', 'dir /P "D:\\Program Files\\"'],
  ['dir D:\\Program Files\\ && dir C:\\Program Files\\', 'dir "D:\\Program Files\\" && dir "C:\\Program Files\\"'],
];

const lsCases: Case[] = [
  ['ls D:\\Program Files\\', 'dir "D:\\Program Files\\"'],
  ['ls "D:\\Program Files\\"', 'dir "D:\\Program Files\\"'],
  ['LS "D:\\Program Files\\"', 'dir "D:\\Program Files\\"'],
  ['ls D:\\Program Files\\ && ls C:\\Program Files\\', 'dir "D:\\Program Files\\" && dir "C:\\Program Files\\"'],
];

const moveCases: Case[] = [
  ['move D:\\Program Files\\file.txt C:\\Program Files\\file.txt', 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
  ['move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"', 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
  ['MOVE "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"', 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
];

const mvCases: Case[] = [
  ['mv D:\\Program Files\\file.txt C:\\Program Files\\file.txt', 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
  ['mv "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"', 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
  ['MV "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"', 'move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"'],
];

const typeCases: Case[] = [
  ['type D:\\Program Files\\file.txt', 'type "D:\\Program Files\\file.txt"'],
  ['type "D:\\Program Files\\file.txt"', 'type "D:\\Program Files\\file.txt"'],
  ['TYPE "D:\\Program Files\\file.txt"', 'type "D:\\Program Files\\file.txt"'],
  ['type D:\\Program Files\\file.txt && type C:\\Program Files\\file.txt', 'type "D:\\Program Files\\file.txt" && type "C:\\Program Files\\file.txt"'],
];

const catCases: Case[] = [
  ['cat D:\\Program Files\\file.txt', 'type "D:\\Program Files\\file.txt"'],
  ['cat "D:\\Program Files\\file.txt"', 'type "D:\\Program Files\\file.txt"'],
  ['CAT "D:\\Program Files\\file.txt"', 'type "D:\\Program Files\\file.txt"'],
];

const mkdirCases: Case[] = [
  ['mkdir D:\\Program Files\\NewFolder', 'mkdir "D:\\Program Files\\NewFolder"'],
  ['mkdir "D:\\Program Files\\NewFolder"', 'mkdir "D:\\Program Files\\NewFolder"'],
  ['MKDIR "D:\\Program Files\\NewFolder"', 'mkdir "D:\\Program Files\\NewFolder"'],
  ['md D:\\Program Files\\NewFolder', 'mkdir "D:\\Program Files\\NewFolder"'],
  ['mkdir D:\\Program Files\\A && mkdir D:\\Program Files\\B', 'mkdir "D:\\Program Files\\A" && mkdir "D:\\Program Files\\B"'],
];

const rmdirCases: Case[] = [
  ['rmdir D:\\Program Files\\OldFolder', 'rmdir "D:\\Program Files\\OldFolder"'],
  ['rmdir "D:\\Program Files\\OldFolder"', 'rmdir "D:\\Program Files\\OldFolder"'],
  ['RMDIR "D:\\Program Files\\OldFolder"', 'rmdir "D:\\Program Files\\OldFolder"'],
  ['rd D:\\Program Files\\OldFolder', 'rmdir "D:\\Program Files\\OldFolder"'],
  ['rmdir /S /Q D:\\Program Files\\OldFolder', 'rmdir /S /Q "D:\\Program Files\\OldFolder"'],
  ['rmdir D:\\Program Files\\A && rmdir D:\\Program Files\\B', 'rmdir "D:\\Program Files\\A" && rmdir "D:\\Program Files\\B"'],
];

const renameCases: Case[] = [
  ['rename D:\\Program Files\\old.txt new.txt', 'ren "D:\\Program Files\\old.txt" new.txt'],
  ['rename "D:\\Program Files\\old.txt" new.txt', 'ren "D:\\Program Files\\old.txt" new.txt'],
  ['RENAME "D:\\Program Files\\old.txt" new.txt', 'ren "D:\\Program Files\\old.txt" new.txt'],
  ['ren D:\\Program Files\\old.txt new.txt', 'ren "D:\\Program Files\\old.txt" new.txt'],
];

const echoCases: Case[] = [
  ['echo hello world', 'echo hello world'],
  ['echo hello && echo world', 'echo hello && echo world'],
  ['echo hello > output.txt', 'echo hello > output.txt'],
  ['echo hello >> output.txt', 'echo hello >> output.txt'],
  ['echo hello | find "h"', 'echo hello | find "h"'],
];

const findCases: Case[] = [
  ['find "hello" D:\\Program Files\\file.txt', 'find "hello" "D:\\Program Files\\file.txt"'],
  ['find "hello" "D:\\Program Files\\file.txt"', 'find "hello" "D:\\Program Files\\file.txt"'],
  ['find /I "hello" D:\\Program Files\\file.txt', 'find /I "hello" "D:\\Program Files\\file.txt"'],
];

const findstrCases: Case[] = [
  ['findstr "pattern" D:\\Program Files\\file.txt', 'findstr "pattern" "D:\\Program Files\\file.txt"'],
  ['findstr /R "pattern" D:\\Program Files\\file.txt', 'findstr /R "pattern" "D:\\Program Files\\file.txt"'],
  ['grep "pattern" D:\\Program Files\\file.txt', 'findstr "pattern" "D:\\Program Files\\file.txt"'],
];

const clsCases: Case[] = [
  ['cls', 'cls'],
  ['clear', 'cls'],
  ['cls && dir D:\\Program Files\\', 'cls && dir "D:\\Program Files\\"'],
  ['clear && dir D:\\Program Files\\', 'cls && dir "D:\\Program Files\\"'],
];

const moreCases: Case[] = [
  ['more D:\\Program Files\\file.txt', 'more "D:\\Program Files\\file.txt"'],
  ['more "D:\\Program Files\\file.txt"', 'more "D:\\Program Files\\file.txt"'],
];

const xcopyCases: Case[] = [
  ['xcopy D:\\Program Files\\src D:\\Program Files\\dst', 'xcopy "D:\\Program Files\\src" "D:\\Program Files\\dst"'],
  ['xcopy "D:\\Program Files\\src" "D:\\Program Files\\dst"', 'xcopy "D:\\Program Files\\src" "D:\\Program Files\\dst"'],
  ['xcopy /S /E D:\\Program Files\\src D:\\Program Files\\dst', 'xcopy /S /E "D:\\Program Files\\src" "D:\\Program Files\\dst"'],
];

const pushdCases: Case[] = [
  ['pushd D:\\Program Files\\', 'pushd "D:\\Program Files\\"'],
  ['pushd "D:\\Program Files\\"', 'pushd "D:\\Program Files\\"'],
];

const popdCases: Case[] = [
  ['popd', 'popd'],
  ['popd && dir D:\\Program Files\\', 'popd && dir "D:\\Program Files\\"'],
];

const whereCases: Case[] = [
  ['where python', 'where python'],
  ['which python', 'where python'],
];

const rmCases: Case[] = [
  ['rm D:\\Program Files\\file.txt', 'del "D:\\Program Files\\file.txt"'],
  ['rm "D:\\Program Files\\file.txt"', 'del "D:\\Program Files\\file.txt"'],
  ['rm -rf D:\\Program Files\\OldFolder', 'rmdir /s /q "D:\\Program Files\\OldFolder"'],
  ['rm -rf "D:\\Program Files\\OldFolder"', 'rmdir /s /q "D:\\Program Files\\OldFolder"'],
  ['rm -r D:\\Program Files\\OldFolder', 'rmdir /s "D:\\Program Files\\OldFolder"'],
];

describe('fixCmd', () => {
  describe('cd', () => { test.each(cdCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('copy', () => { test.each(copyCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('cp', () => { test.each(cpCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('del', () => { test.each(delCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('dir', () => { test.each(dirCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('ls', () => { test.each(lsCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('move', () => { test.each(moveCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('mv', () => { test.each(mvCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('type', () => { test.each(typeCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('cat', () => { test.each(catCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('mkdir', () => { test.each(mkdirCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('rmdir', () => { test.each(rmdirCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('rename', () => { test.each(renameCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('echo', () => { test.each(echoCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('find', () => { test.each(findCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('findstr', () => { test.each(findstrCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('cls', () => { test.each(clsCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('more', () => { test.each(moreCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('xcopy', () => { test.each(xcopyCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('pushd', () => { test.each(pushdCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('popd', () => { test.each(popdCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('where', () => { test.each(whereCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
  describe('rm', () => { test.each(rmCases)('%s', (i, e) => expect(fixCmd(i)).toBe(e)); });
});
