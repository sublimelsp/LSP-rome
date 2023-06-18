# LSP-rome

[Rome](https://rome.tools/) unifies your development stack by combining the functionality of separate tools. It uses a single configuration file, has fantastic performance, and works with any stack. This package enables Sublime Text integration so that you can:
 - Format files on save or when issuing the `LSP: Format Document` command
 - See linting hints while you type and apply code fixes
 - Perform refactors

The package supports JavaScript and TypeScript files.

## Installation

1. Install [LSP](https://packagecontrol.io/packages/LSP) and [LSP-rome](https://packagecontrol.io/packages/LSP-rome) via Package Control.
2. (Optional but recommended) Install [LSP-file-watcher-chokidar](https://github.com/sublimelsp/LSP-file-watcher-chokidar) via Package Control to enable functionality to notify the server about changes to the `rome.json` configuration file.
3. Restart Sublime.

## Configuration

Open the configuration file using the Command Palette `Preferences: LSP-rome Settings` command or from the Sublime menu.

> Note:
> By default the package requires a Rome configuration file (`rome.json`) in the root of the project to enable syntax errors, formatting and linting. This can be changed through the `rome.requireConfiguration` option in `Preferences: LSP-rome Settings`.

## Rome Resolution

The package tries to use Rome from your project's local dependencies (`node_modules/rome`). We recommend adding Rome as a project dependency to ensure that NPM scripts and the extension use the same Rome version.

You can also explicitly specify the `rome` binary the extension should use by configuring the `rome.lspBin` setting in `LSP-rome` Settings.

If the project has no dependency on Rome and no explicit path is configured, the extension uses the Rome version managed by this package.

## Usage

### Format document

To format an entire document, open the _Command Palette_ (<kbd>Ctrl</kbd>/<kbd title="Cmd">⌘</kbd>+<kbd title="Shift">⇧</kbd>+<kbd>P</kbd>) and select `LSP: Format Document`.

To format a text range, select the text you want to format, open the _Command Palette_ (<kbd>Ctrl</kbd>/<kbd title="Cmd">⌘</kbd>+<kbd title="Shift">⇧</kbd>+<kbd>P</kbd>), and select `LSP: Format Selection`.

### Format on save

To enable format on save, open the `Preferences: LSP Settings` from the _Command Palette_ and set or edit the `lsp_code_actions_on_save` option:

```json
s
```

### Fix on save

To enable fix on save, open `Preferences: LSP Settings` from the _Command Palette_ and set or edit the `lsp_code_actions_on_save: { "quickfix.rome": true }` option.

### Imports Sorting [Experimental]

Rome has experimental support for imports sorting through the "Organize Imports" code action. This action is accessible through the _Command Palette_ (<kbd>Ctrl</kbd>/<kbd title="Cmd">⌘</kbd>+<kbd title="Shift">⇧</kbd>+<kbd>P</kbd>) by selecting `LSP-rome: Organize Imports`.

Currently, this functionality needs to be explicitly enabled in the `rome.json` configuration file:

```json
{
    "organizeImports": {
        "enabled": true
    }
}
```

You can add the following to `Preferences: LSP Settings` if you want the action to run automatically on save instead of calling it manually:

```json
{
    "lsp_code_actions_on_save":{
        "source.organizeImports.rome": true
    }
}
```
