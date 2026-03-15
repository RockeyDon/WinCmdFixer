import { splitArgs } from '../src/args';

const testCases: [string, string[]][] = [
  // basic splitting
  ['hello world', ['hello', 'world']],
  ['  hello   world  ', ['hello', 'world']],
  // quoted strings
  ['"hello world"', ['hello world']],
  ["'hello world'", ['hello world']],
  // escape with ^
  ['hello^ world', ['hello world']],
  // empty quoted string
  ['""', ['']],
  // mixed
  ['copy "C:\\Program Files\\file.txt" D:\\dest', ['copy', 'C:\\Program Files\\file.txt', 'D:\\dest']],
];

describe('splitArgs', () => {
  test.each(testCases)('splitArgs(%j)', (input, expected) => {
    expect(splitArgs(input)).toEqual(expected);
  });
});
