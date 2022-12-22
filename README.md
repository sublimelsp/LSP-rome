# LSP-rome

Rome LSP server for Sublime LSP provided through [Rome](https://rome.tools/).

## Installation

1. Install [LSP](https://packagecontrol.io/packages/LSP) and [LSP-rome](https://packagecontrol.io/packages/LSP-rome) via Package Control.
2. (Optional but recommended) Install [LSP-file-watcher-chokidar](https://github.com/sublimelsp/LSP-file-watcher-chokidar) via Package Control to enable functionality to notify the server about changes to `rome.json` configuration file.
3. Restart Sublime.

### Configuration

Open the configuration file using the Command Palette `Preferences: LSP-rome Settings` command or from the Sublime menu.

#### languages

Defines on which types of files the ESLint server will run.

