export interface CommandContext {
  openUrl: (url: string) => void;
}

export type CommandHandler = (context: CommandContext) => void | Promise<void>;

interface CommandBase {
  name: string;
}

export interface PublicLink extends CommandBase {
  kind: 'public-link';
  label: string;
  path: string;
  href: string;
  a11y: string;
  svg: string;
}

export interface PublicCommand extends CommandBase {
  kind: 'public-command';
  execute: CommandHandler;
}

export interface PrivateCommand extends CommandBase {
  kind: 'private-command';
  execute: CommandHandler;
}

export type CommandEntry = PublicLink | PublicCommand | PrivateCommand;

const email = 'rukna1000@gmail.com';

// Public links are the fully discoverable entries: they render in the table,
// participate in autocomplete, execute from the prompt, and receive a matching
// `/<name>` shortcut at build time.
export const publicLinks = [
  {
    kind: 'public-link',
    name: 'github',
    label: 'GitHub',
    path: '/goobta',
    href: 'https://github.com/goobta',
    a11y: 'GitHub, github.com/goobta',
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>`,
  },
  {
    kind: 'public-link',
    name: 'linkedin',
    label: 'LinkedIn',
    path: '/in/goobta',
    href: 'https://www.linkedin.com/in/goobta/',
    a11y: 'LinkedIn, linkedin.com/in/goobta',
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>`,
  },
  {
    kind: 'public-link',
    name: 'email',
    label: 'Email',
    path: email,
    href: `mailto:${email}`,
    a11y: `Email, ${email}`,
    svg: `<svg viewBox="0 0 512 512" aria-hidden="true" focusable="false"><path fill="currentColor" d="M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48L48 64zM0 176L0 384c0 35.3 28.7 64 64 64l384 0c35.3 0 64-28.7 64-64l0-208L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z"/></svg>`,
  },
  {
    kind: 'public-link',
    name: 'strava',
    label: 'Strava',
    path: '/athletes/115751174',
    href: 'https://www.strava.com/athletes/115751174',
    a11y: 'Strava, strava.com/athletes/115751174',
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M15.387 17.944l-2.089-4.116h-3.065L15.387 24l5.15-10.172h-3.066m-7.008-5.599l2.836 5.598h4.172L10.463 0l-7 13.828h4.169"/></svg>`,
  },
  {
    kind: 'public-link',
    name: 'spotify',
    label: 'Spotify',
    path: '/user/theultimatepanda',
    href: 'https://open.spotify.com/user/theultimatepanda',
    a11y: 'Spotify, open.spotify.com/user/theultimatepanda',
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 0C5.4 0 0 5.4 0 12s5.4 12 12 12 12-5.4 12-12S18.66 0 12 0zm5.521 17.34c-.24.359-.66.48-1.021.24-2.82-1.74-6.36-2.101-10.561-1.141-.418.122-.779-.179-.899-.539-.12-.421.18-.78.54-.9 4.56-1.021 8.52-.6 11.64 1.32.42.18.479.659.301 1.02zm1.44-3.3c-.301.42-.841.6-1.262.3-3.239-1.98-8.159-2.58-11.939-1.38-.479.12-1.02-.12-1.14-.6-.12-.48.12-1.021.6-1.141C9.6 9.9 15 10.561 18.72 12.84c.361.181.54.78.241 1.2zm.12-3.36C15.24 8.4 8.82 8.16 5.16 9.301c-.6.179-1.2-.181-1.38-.721-.18-.601.18-1.2.72-1.381 4.26-1.26 11.28-1.02 15.721 1.621.539.3.719 1.02.419 1.56-.299.421-1.02.599-1.559.3z"/></svg>`,
  },
  {
    kind: 'public-link',
    name: 'venmo',
    label: 'Venmo',
    path: '/u/agupta628',
    href: 'https://venmo.com/u/agupta628',
    a11y: 'Venmo, venmo.com/u/agupta628',
    svg: `<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M4.0 4.6 L10.3 4.0 L11.6 15.2 C13.6 11.9 14.5 8.3 13.5 5.0 L19.4 3.8 C21.2 7.3 20.6 12.1 17.5 16.4 C16.1 18.4 14.7 19.8 13.5 20.6 L6.6 20.6 Z"/></svg>`,
  },
] as const satisfies readonly PublicLink[];

// Public commands are discoverable in autocomplete and executable from the
// prompt, but never appear in the link table or receive shortcut pages.
export const publicCommands = [] as const satisfies readonly PublicCommand[];

// Private commands are executable only. They are intentionally absent from the
// table, autocomplete, and generated shortcut pages; this is obscurity, not an
// authentication boundary, because the handlers ship to the browser.
export const privateCommands = [
  {
    kind: 'private-command',
    name: 'mcp',
    execute: ({ openUrl }) => openUrl('https://mcp.goobta.io/login'),
  },
] as const satisfies readonly PrivateCommand[];

export const commandEntries: readonly CommandEntry[] = [
  ...publicLinks,
  ...publicCommands,
  ...privateCommands,
];

const commandNamePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const names = new Set<string>();

for (const command of commandEntries) {
  if (!commandNamePattern.test(command.name)) {
    throw new Error(`Invalid command name "${command.name}": use lowercase URL-safe names only.`);
  }
  if (names.has(command.name)) {
    throw new Error(`Duplicate command name "${command.name}".`);
  }
  names.add(command.name);
}

const commandsByName = new Map(commandEntries.map((command) => [command.name, command]));

export const autocompleteNames = [...publicLinks, ...publicCommands].map(
  (command) => command.name,
);

export const hasCommand = (name: string) => commandsByName.has(name);

export async function executeCommand(name: string, context: CommandContext): Promise<boolean> {
  const command = commandsByName.get(name);
  if (!command) return false;

  if (command.kind === 'public-link') {
    context.openUrl(command.href);
  } else {
    await command.execute(context);
  }

  return true;
}
