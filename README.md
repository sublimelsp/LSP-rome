# LSP-rome

[Rome](https://rome.tools/) is a unified linter and formatter for JavaScript and TypeScript files.

This package enables Sublime Text integration so that you can:
 - Format files on save or when issuing the `LSP: Format Document` command
 - See linting hints while you type and apply code fixes
 - Perform refactors

## Installation

1. Install [LSP](https://packagecontrol.io/packages/LSP) and [LSP-rome](https://packagecontrol.io/packages/LSP-rome) via Package Control.
2. (Optional but recommended) Install [LSP-file-watcher-chokidar](https://github.com/sublimelsp/LSP-file-watcher-chokidar) via Package Control to enable functionality to notify the server about changes to the `rome.json` configuration file.
3. Restart Sublime.

### Configuration

Open the configuration file using the Command Palette `Preferences: LSP-rome Settings` command or from the Sublime menu.

## Rome Resolution

The package tries to use Rome from your project's local dependencies (`node_modules/rome`). We recommend adding Rome as a project dependency to ensure that NPM scripts and the extension use the same Rome version.

You can also explicitly specify the `rome` binary the extension should use by configuring the `rome.lspBin` setting in `LSP-rome` Settings.

If the project has no dependency on Rome and no explicit path is configured, the extension uses the Rome version managed by this package.
