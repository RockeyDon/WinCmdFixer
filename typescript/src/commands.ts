import { splitArgs } from './args';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type ParsedResult = [string, string];
export type ParseFunc = (text: string, kind: string) => ParsedResult;
export type ShellKind = 'cmd' | 'powershell' | 'unix';

// ---------------------------------------------------------------------------
// Registry
// ---------------------------------------------------------------------------

const COMMAND_REGISTRY: Record<string, ParseFunc> = {};

/** CMD / PS5 separators.  '&&' and '||' are CMD-only; PS5 uses ';'. */
export const SEPARATORS = ['&', '&&', '|', '||', '>', '>>', '<'];

const RE_DRIVE = /[A-Za-z]:\\/;

// ---------------------------------------------------------------------------
// PathState
// ---------------------------------------------------------------------------

enum PathState {
  START_NEW = 1,
  END_CURRENT = 2,
  CONTINUE = 3,
}

type Classifier = (p: string) => PathState;

// ---------------------------------------------------------------------------
// Public lookup
// ---------------------------------------------------------------------------

export function getParseFunc(name: string): ParseFunc | null {
  if (SEPARATORS.includes(name)) {
    return parseSeparator(name);
  }
  return COMMAND_REGISTRY[name] ?? null;
}

// ---------------------------------------------------------------------------
// Decorator-like helper (register command names)
// ---------------------------------------------------------------------------

function command(names: string[], fn: ParseFunc): ParseFunc {
  for (const n of names) {
    COMMAND_REGISTRY[n] = fn;
  }
  return fn;
}

// ---------------------------------------------------------------------------
// Separator handling
// ---------------------------------------------------------------------------

const PS_SEPARATOR_MAP: Record<string, string> = {
  '&&': ';',
  '||': ';',
  '&': ';',
};

function translateSeparator(sep: string, kind: string): string {
  if (kind === 'powershell') {
    return PS_SEPARATOR_MAP[sep] ?? sep;
  }
  return sep;
}

function parseSeparator(name: string): ParseFunc {
  return (_text: string, kind: string): ParsedResult => {
    return [translateSeparator(name, kind), _text];
  };
}

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

function fmtCmd(name: string, args: string[]): string {
  if (args.length > 0) {
    return `${name} ${args.join(' ')}`;
  }
  return name;
}

function parseCommon(
  text: string,
  classify: Classifier,
): [string[], string] {
  if (!text || !text.trim()) {
    return [[], ''];
  }

  // Input is always Windows-style (broken CMD), so always parse with '^'.
  const parts = splitArgs(text, '^');
  const args: string[] = [];
  let inPathname = false;
  let containTail = true;
  let i = 0;

  for (i = 0; i < parts.length; i++) {
    const p = parts[i];

    if (SEPARATORS.includes(p)) {
      containTail = false;
      break;
    }

    const state = classify(p);

    if (!inPathname && state === PathState.START_NEW) {
      inPathname = true;
      args.push(p);
    } else if (!inPathname && state === PathState.END_CURRENT) {
      if (p in COMMAND_REGISTRY) {
        containTail = false;
        break;
      }
      args.push(p);
    } else if (!inPathname && state === PathState.CONTINUE) {
      if (p in COMMAND_REGISTRY) {
        containTail = false;
        break;
      }
      args.push(p);
    } else if (inPathname && state === PathState.START_NEW) {
      args[args.length - 1] = `"${args[args.length - 1]}"`;
      args.push(p);
    } else if (inPathname && state === PathState.CONTINUE) {
      args[args.length - 1] += ` ${p}`;
    } else if (inPathname && state === PathState.END_CURRENT) {
      inPathname = false;
      args[args.length - 1] = `"${args[args.length - 1]}"`;
      args.push(p);
    }
  }

  if (inPathname) {
    args[args.length - 1] = `"${args[args.length - 1]}"`;
  }

  const remaining = containTail ? parts.slice(i + 1) : parts.slice(i);
  return [args, remaining.join(' ')];
}

function winPathToUnix(arg: string): string {
  if (!RE_DRIVE.test(arg)) {
    return arg;
  }
  const stripped = arg.replace(/^["']|["']$/g, '');
  const drive = stripped[0].toLowerCase();
  const unixPath = stripped.slice(3).replace(/\\/g, '/');
  return `"/${drive}/${unixPath}"`;
}

// ---------------------------------------------------------------------------
// Standard classifiers
// ---------------------------------------------------------------------------

function judgeStandard(p: string): PathState {
  if (p.startsWith('/')) return PathState.END_CURRENT;
  if (RE_DRIVE.test(p)) return PathState.START_NEW;
  return PathState.CONTINUE;
}

function judgeUnixOpts(p: string): PathState {
  if (p.startsWith('/') || p.startsWith('-')) return PathState.END_CURRENT;
  if (RE_DRIVE.test(p)) return PathState.START_NEW;
  return PathState.CONTINUE;
}

function judgeNoOption(p: string): PathState {
  if (RE_DRIVE.test(p)) return PathState.START_NEW;
  return PathState.CONTINUE;
}

// ---------------------------------------------------------------------------
// Helper: remove a flag (case-insensitive) from args
// ---------------------------------------------------------------------------

function removeFlagCI(args: string[], flag: string): boolean {
  const lower = flag.toLowerCase();
  for (let i = 0; i < args.length; i++) {
    if (args[i].toLowerCase() === lower) {
      args.splice(i, 1);
      return true;
    }
  }
  return false;
}

// ---------------------------------------------------------------------------
// Command definitions
// ---------------------------------------------------------------------------

command(['cd'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);
  removeFlagCI(args, '/d');

  if (kind === 'cmd') {
    const prefix = args.length > 0 ? 'cd /d' : 'cd';
    return [fmtCmd(prefix, args), remaining];
  }
  if (kind === 'powershell') {
    return [fmtCmd('Set-Location', args), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('cd', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['copy'], (text: string, kind: string): ParsedResult => {
  function judge(p: string): PathState {
    if (p.startsWith('/') || p === '+') return PathState.END_CURRENT;
    if (RE_DRIVE.test(p)) return PathState.START_NEW;
    return PathState.CONTINUE;
  }

  const [args, remaining] = parseCommon(text, judge);

  if (kind === 'cmd') {
    return [fmtCmd('copy', args), remaining];
  }
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/') && a !== '+');
    return [fmtCmd('Copy-Item', psArgs), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('cp', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['cp'], (text: string, kind: string): ParsedResult => {
  function judge(p: string): PathState {
    if (p.startsWith('/') || p === '+' || p.startsWith('-'))
      return PathState.END_CURRENT;
    if (RE_DRIVE.test(p)) return PathState.START_NEW;
    return PathState.CONTINUE;
  }

  const [args, remaining] = parseCommon(text, judge);

  if (kind === 'cmd') {
    const idx = args.indexOf('-r');
    if (idx !== -1) {
      args.splice(idx, 1);
      return [fmtCmd('robocopy /e', args), remaining];
    }
    return [fmtCmd('copy', args), remaining];
  }
  if (kind === 'powershell') {
    const idx = args.indexOf('-r');
    const recurse = idx !== -1;
    if (recurse) args.splice(idx, 1);
    const suffix = recurse ? ' -Recurse' : '';
    return [fmtCmd('Copy-Item', args) + suffix, remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('cp', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['del'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') {
    return [fmtCmd('del', args), remaining];
  }
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    return [fmtCmd('Remove-Item', psArgs), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('rm', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['rm'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeUnixOpts);

  const hasR = removeFlagCI(args, '-r');
  const hasF = removeFlagCI(args, '-f');
  const hasRF = removeFlagCI(args, '-rf');
  const recursive = hasR || hasRF;
  const force = hasF || hasRF;

  if (kind === 'cmd') {
    if (recursive) {
      let flags = '/s';
      if (force) flags += ' /q';
      return [fmtCmd(`rmdir ${flags}`, args), remaining];
    }
    return [fmtCmd('del', args), remaining];
  }
  if (kind === 'powershell') {
    let suffix = '';
    if (recursive) suffix += ' -Recurse';
    if (force) suffix += ' -Force';
    return [fmtCmd('Remove-Item', args) + suffix, remaining];
  }
  if (kind === 'unix') {
    let flags = '';
    if (recursive) flags += '-r';
    if (force) flags += flags ? 'f' : '-f';
    const unixArgs = args.map(winPathToUnix);
    if (flags) {
      return [fmtCmd(`rm ${flags}`, unixArgs), remaining];
    }
    return [fmtCmd('rm', unixArgs), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['dir', 'ls'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') {
    return [fmtCmd('dir', args), remaining];
  }
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    return [fmtCmd('Get-ChildItem', psArgs), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('ls', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['move', 'mv'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') {
    return [fmtCmd('move', args), remaining];
  }
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    return [fmtCmd('Move-Item', psArgs), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('mv', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['type', 'cat'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeNoOption);

  if (kind === 'cmd') {
    return [fmtCmd('type', args), remaining];
  }
  if (kind === 'powershell') {
    return [fmtCmd('Get-Content', args), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('cat', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['mkdir', 'md'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') {
    return [fmtCmd('mkdir', args), remaining];
  }
  if (kind === 'powershell') {
    return [fmtCmd('New-Item -ItemType Directory -Path', args), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('mkdir', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['rmdir', 'rd'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') {
    return [fmtCmd('rmdir', args), remaining];
  }
  if (kind === 'powershell') {
    const hasS = removeFlagCI(args, '/s');
    removeFlagCI(args, '/q');
    const psArgs = args.filter(a => !a.startsWith('/'));
    const suffix = hasS ? ' -Recurse -Force' : '';
    return [fmtCmd('Remove-Item', psArgs) + suffix, remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('rmdir', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['rename', 'ren'], (text: string, kind: string): ParsedResult => {
  if (!text || !text.trim()) {
    if (kind === 'powershell') return ['Rename-Item', ''];
    if (kind === 'unix') return ['mv', ''];
    return ['ren', ''];
  }

  const parts = splitArgs(text, '^');
  const args: string[] = [];
  let inPathname = false;
  let firstPathDone = false;
  let remainingParts: string[] = [];

  for (let i = 0; i < parts.length; i++) {
    const p = parts[i];

    if (SEPARATORS.includes(p)) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
      }
      remainingParts = parts.slice(i);
      break;
    }

    if (firstPathDone) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
      }
      args.push(p);
      continue;
    }

    const state = judgeStandard(p);

    if (!inPathname && state === PathState.START_NEW) {
      inPathname = true;
      args.push(p);
    } else if (!inPathname) {
      args.push(p);
    } else if (inPathname && state === PathState.START_NEW) {
      args[args.length - 1] = `"${args[args.length - 1]}"`;
      firstPathDone = true;
      args.push(p);
      inPathname = true;
    } else if (inPathname && state === PathState.CONTINUE) {
      if (!p.includes('\\') && !RE_DRIVE.test(p) && !p.includes('/')) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
        firstPathDone = true;
        args.push(p);
      } else {
        args[args.length - 1] += ` ${p}`;
      }
    } else if (inPathname && state === PathState.END_CURRENT) {
      inPathname = false;
      args[args.length - 1] = `"${args[args.length - 1]}"`;
      firstPathDone = true;
      args.push(p);
    }
  }

  if (inPathname) {
    args[args.length - 1] = `"${args[args.length - 1]}"`;
  }

  const remaining = remainingParts.join(' ');

  if (kind === 'cmd') return [fmtCmd('ren', args), remaining];
  if (kind === 'powershell') return [fmtCmd('Rename-Item', args), remaining];
  if (kind === 'unix') return [fmtCmd('mv', args.map(winPathToUnix)), remaining];
  throw new Error(`unknown kind: ${kind}`);
});

command(['echo'], (text: string, kind: string): ParsedResult => {
  if (!text || !text.trim()) {
    return kind === 'powershell' ? ['Write-Output', ''] : ['echo', ''];
  }

  const tokens = text.split(/\s+/).filter(t => t.length > 0);
  const msgParts: string[] = [];
  const restParts: string[] = [];
  let hitSep = false;

  for (const t of tokens) {
    if (SEPARATORS.includes(t) && !hitSep) {
      hitSep = true;
    }
    if (hitSep) {
      restParts.push(t);
    } else {
      msgParts.push(t);
    }
  }

  const message = msgParts.join(' ');
  const remaining = restParts.join(' ');

  if (kind === 'cmd') return [`echo ${message}`, remaining];
  if (kind === 'powershell') return [`Write-Output ${message}`, remaining];
  if (kind === 'unix') return [`echo ${message}`, remaining];
  throw new Error(`unknown kind: ${kind}`);
});

command(['find'], (text: string, kind: string): ParsedResult => {
  if (!text || !text.trim()) {
    if (kind === 'powershell') return ['Select-String', ''];
    if (kind === 'unix') return ['grep', ''];
    return ['find', ''];
  }

  const tokens = text.split(/\s+/).filter(t => t.length > 0);
  const args: string[] = [];
  const remainingParts: string[] = [];
  let hitSep = false;
  let inPathname = false;

  for (const t of tokens) {
    if (hitSep) {
      remainingParts.push(t);
      continue;
    }
    if (SEPARATORS.includes(t)) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
      }
      hitSep = true;
      remainingParts.push(t);
      continue;
    }

    if (t.startsWith('"') || t.startsWith('/')) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
      }
      args.push(t);
    } else if (RE_DRIVE.test(t)) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
      }
      inPathname = true;
      args.push(t);
    } else {
      if (inPathname) {
        args[args.length - 1] += ` ${t}`;
      } else {
        args.push(t);
      }
    }
  }

  if (inPathname) {
    args[args.length - 1] = `"${args[args.length - 1]}"`;
  }

  const remaining = remainingParts.join(' ');

  if (kind === 'cmd') return [fmtCmd('find', args), remaining];
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    return [fmtCmd('Select-String', psArgs), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('grep', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['findstr', 'grep'], (text: string, kind: string): ParsedResult => {
  if (!text || !text.trim()) {
    if (kind === 'powershell') return ['Select-String', ''];
    if (kind === 'unix') return ['grep', ''];
    return ['findstr', ''];
  }

  const tokens = text.split(/\s+/).filter(t => t.length > 0);
  const args: string[] = [];
  const remainingParts: string[] = [];
  let hitSep = false;
  let inPathname = false;

  for (const t of tokens) {
    if (hitSep) {
      remainingParts.push(t);
      continue;
    }
    if (SEPARATORS.includes(t)) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
      }
      hitSep = true;
      remainingParts.push(t);
      continue;
    }

    if (t.startsWith('"') || t.startsWith('/') || t.startsWith('-')) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
        inPathname = false;
      }
      args.push(t);
    } else if (RE_DRIVE.test(t)) {
      if (inPathname) {
        args[args.length - 1] = `"${args[args.length - 1]}"`;
      }
      inPathname = true;
      args.push(t);
    } else {
      if (inPathname) {
        args[args.length - 1] += ` ${t}`;
      } else {
        args.push(t);
      }
    }
  }

  if (inPathname) {
    args[args.length - 1] = `"${args[args.length - 1]}"`;
  }

  const remaining = remainingParts.join(' ');

  if (kind === 'cmd') return [fmtCmd('findstr', args), remaining];
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/') && !a.startsWith('-'));
    return [fmtCmd('Select-String', psArgs), remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('grep', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['cls', 'clear'], (_text: string, kind: string): ParsedResult => {
  const remaining = _text ? _text.trim() : '';
  if (kind === 'cmd') return ['cls', remaining];
  if (kind === 'powershell') return ['Clear-Host', remaining];
  if (kind === 'unix') return ['clear', remaining];
  throw new Error(`unknown kind: ${kind}`);
});

command(['more'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') return [fmtCmd('more', args), remaining];
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    const psStr = psArgs.join(' ');
    return [
      psStr ? `Get-Content ${psStr} | Out-Host -Paging` : 'Get-Content | Out-Host -Paging',
      remaining,
    ];
  }
  if (kind === 'unix') {
    return [fmtCmd('more', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['xcopy'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') return [fmtCmd('xcopy', args), remaining];
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    return [fmtCmd('Copy-Item', psArgs) + ' -Recurse', remaining];
  }
  if (kind === 'unix') {
    return [fmtCmd('cp -r', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['pushd'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') return [fmtCmd('pushd', args), remaining];
  if (kind === 'powershell') return [fmtCmd('Push-Location', args), remaining];
  if (kind === 'unix') {
    return [fmtCmd('pushd', args.map(winPathToUnix)), remaining];
  }
  throw new Error(`unknown kind: ${kind}`);
});

command(['popd'], (_text: string, kind: string): ParsedResult => {
  const remaining = _text ? _text.trim() : '';
  if (kind === 'cmd') return ['popd', remaining];
  if (kind === 'powershell') return ['Pop-Location', remaining];
  if (kind === 'unix') return ['popd', remaining];
  throw new Error(`unknown kind: ${kind}`);
});

command(['where', 'which'], (text: string, kind: string): ParsedResult => {
  const [args, remaining] = parseCommon(text, judgeStandard);

  if (kind === 'cmd') return [fmtCmd('where', args), remaining];
  if (kind === 'powershell') {
    const psArgs = args.filter(a => !a.startsWith('/'));
    return [fmtCmd('Get-Command', psArgs), remaining];
  }
  if (kind === 'unix') return [fmtCmd('which', args), remaining];
  throw new Error(`unknown kind: ${kind}`);
});
