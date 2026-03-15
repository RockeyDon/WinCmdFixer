import { fixUnixShell } from '../src';

type Case = [string, string];

const cdCases: Case[] = [
  ['cd D:\\Program Files\\', 'cd "/d/Program Files/"'],
  ['cd "D:\\Program Files\\"', 'cd "/d/Program Files/"'],
  ['CD "D:\\Program Files\\"', 'cd "/d/Program Files/"'],
  ['cd /D D:\\Program Files\\', 'cd "/d/Program Files/"'],
  ['cd D:\\Program Files\\ && cd C:\\Program Files\\', 'cd "/d/Program Files/" && cd "/c/Program Files/"'],
];

const copyCases: Case[] = [
  ['copy D:\\Program Files\\file.txt C:\\Program Files\\', 'cp "/d/Program Files/file.txt" "/c/Program Files/"'],
  ['copy "D:\\Program Files\\file.txt" "C:\\Program Files\\"', 'cp "/d/Program Files/file.txt" "/c/Program Files/"'],
];

const cpCases: Case[] = [
  ['cp D:\\Program Files\\file.txt C:\\Program Files\\', 'cp "/d/Program Files/file.txt" "/c/Program Files/"'],
  ['cp "D:\\Program Files\\file.txt" "C:\\Program Files\\"', 'cp "/d/Program Files/file.txt" "/c/Program Files/"'],
];

const delCases: Case[] = [
  ['del D:\\Program Files\\file.txt', 'rm "/d/Program Files/file.txt"'],
  ['del "D:\\Program Files\\file.txt"', 'rm "/d/Program Files/file.txt"'],
];

const dirCases: Case[] = [
  ['dir D:\\Program Files\\', 'ls "/d/Program Files/"'],
  ['dir "D:\\Program Files\\"', 'ls "/d/Program Files/"'],
  ['dir D:\\Program Files\\ && dir C:\\Program Files\\', 'ls "/d/Program Files/" && ls "/c/Program Files/"'],
];

const lsCases: Case[] = [
  ['ls D:\\Program Files\\', 'ls "/d/Program Files/"'],
  ['ls "D:\\Program Files\\"', 'ls "/d/Program Files/"'],
];

const moveCases: Case[] = [
  ['move D:\\Program Files\\file.txt C:\\Program Files\\file.txt', 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'],
  ['move "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"', 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'],
];

const mvCases: Case[] = [
  ['mv D:\\Program Files\\file.txt C:\\Program Files\\file.txt', 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'],
  ['mv "D:\\Program Files\\file.txt" "C:\\Program Files\\file.txt"', 'mv "/d/Program Files/file.txt" "/c/Program Files/file.txt"'],
];

const typeCases: Case[] = [
  ['type D:\\Program Files\\file.txt', 'cat "/d/Program Files/file.txt"'],
  ['type "D:\\Program Files\\file.txt"', 'cat "/d/Program Files/file.txt"'],
];

const catCases: Case[] = [
  ['cat D:\\Program Files\\file.txt', 'cat "/d/Program Files/file.txt"'],
  ['cat "D:\\Program Files\\file.txt"', 'cat "/d/Program Files/file.txt"'],
];

const newCommandCases: Case[] = [
  ['mkdir D:\\Program Files\\NewFolder', 'mkdir "/d/Program Files/NewFolder"'],
  ['rmdir D:\\Program Files\\OldFolder', 'rmdir "/d/Program Files/OldFolder"'],
  ['rename D:\\Program Files\\old.txt new.txt', 'mv "/d/Program Files/old.txt" new.txt'],
  ['echo hello world', 'echo hello world'],
  ['cls', 'clear'],
  ['clear', 'clear'],
  ['more D:\\Program Files\\file.txt', 'more "/d/Program Files/file.txt"'],
  ['xcopy D:\\Program Files\\src D:\\Program Files\\dst', 'cp -r "/d/Program Files/src" "/d/Program Files/dst"'],
  ['pushd D:\\Program Files\\', 'pushd "/d/Program Files/"'],
  ['popd', 'popd'],
  ['where python', 'which python'],
  ['which python', 'which python'],
  ['find "hello" D:\\Program Files\\file.txt', 'grep "hello" "/d/Program Files/file.txt"'],
  ['findstr "pattern" D:\\Program Files\\file.txt', 'grep "pattern" "/d/Program Files/file.txt"'],
  ['grep "pattern" D:\\Program Files\\file.txt', 'grep "pattern" "/d/Program Files/file.txt"'],
  ['rm -rf D:\\Program Files\\OldFolder', 'rm -rf "/d/Program Files/OldFolder"'],
];

describe('fixUnixShell', () => {
  describe('cd', () => { test.each(cdCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('copy', () => { test.each(copyCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('cp', () => { test.each(cpCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('del', () => { test.each(delCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('dir', () => { test.each(dirCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('ls', () => { test.each(lsCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('move', () => { test.each(moveCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('mv', () => { test.each(mvCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('type', () => { test.each(typeCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('cat', () => { test.each(catCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
  describe('new commands', () => { test.each(newCommandCases)('%s', (i, e) => expect(fixUnixShell(i)).toBe(e)); });
});
