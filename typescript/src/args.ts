/**
 * Split by space, but keep tokens inside quotes together.
 *
 * @param text        - raw argument string.
 * @param escapeChar  - shell-specific escape character
 *                      ('^' for CMD, '`' for PowerShell, '\\' for Unix).
 */
export function splitArgs(text: string, escapeChar: string = '^'): string[] {
  const result: string[] = [];
  let current: string[] = [];
  let inQuotes = false;
  let escaped = false;
  let quoteChar: string | null = null;

  for (let i = 0; i < text.length; i++) {
    const char = text[i];

    if (char === escapeChar && !escaped) {
      escaped = true;
      continue;
    }
    if (escaped) {
      current.push(char);
      escaped = false;
      continue;
    }
    if ((char === '"' || char === "'") && !inQuotes) {
      inQuotes = true;
      quoteChar = char;
      continue;
    }
    if (char === quoteChar && inQuotes) {
      inQuotes = false;
      quoteChar = null;
      if (current.length === 0) {
        result.push('');
      }
      continue;
    }
    if (/\s/.test(char) && !inQuotes) {
      if (current.length > 0) {
        result.push(current.join(''));
        current = [];
      }
      continue;
    }
    current.push(char);
  }

  // last token
  if (current.length > 0) {
    result.push(current.join(''));
  }
  return result;
}
