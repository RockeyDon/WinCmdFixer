import { getParseFunc, SEPARATORS } from './commands';

/** Convert a (possibly broken) command string into valid CMD syntax. */
export function fixCmd(text: string): string {
  return parser(text, 'cmd');
}

/** Convert a (possibly broken) command string into valid PowerShell 5.x syntax. */
export function fixPowershell(text: string): string {
  return parser(text, 'powershell');
}

/** Convert a (possibly broken) command string into valid Unix shell syntax. */
export function fixUnixShell(text: string): string {
  return parser(text, 'unix');
}

/**
 * Main parsing loop.
 *
 * Splits text by the first whitespace to identify a command name, then
 * delegates to the registered parse function.  When a command is not
 * recognised, it is emitted verbatim and the parser continues to look for
 * separators so that subsequent commands can still be fixed.
 */
function parser(text: string, kind: string): string {
  let remaining = text.trim();
  const output: string[] = [];

  while (remaining) {
    const match = remaining.match(/^(\S+)\s*([\s\S]*)$/);
    if (!match) break;

    const first = match[1];
    const others = match[2];

    const parseFunc = getParseFunc(first.toLowerCase());

    if (parseFunc !== null) {
      const [parsedCmd, rest] = parseFunc(others, kind);
      output.push(parsedCmd);
      remaining = rest.trim();
    } else {
      // Unknown command: emit it, then scan forward for a separator
      output.push(first);
      remaining = skipToSeparator(others.trim(), output);
    }
  }

  return output.join(' ');
}

/**
 * Consume tokens until a separator is found, appending them to output.
 * Returns the remaining text starting from the separator token.
 */
function skipToSeparator(text: string, output: string[]): string {
  let remaining = text;

  while (remaining) {
    const match = remaining.match(/^(\S+)\s*([\s\S]*)$/);
    if (!match) break;

    const token = match[1];
    const rest = match[2];

    if (SEPARATORS.includes(token)) {
      return remaining;
    }

    // Check for two-char separators at the start
    for (const sep of ['&&', '||', '>>', '<<']) {
      if (remaining.startsWith(sep)) {
        return remaining;
      }
    }

    output.push(token);
    remaining = rest.trim();
  }

  return '';
}
