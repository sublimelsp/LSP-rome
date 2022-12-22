from LSP.plugin import ClientConfig, WorkspaceFolder
from LSP.plugin.core.typing import List, Optional
from lsp_utils import NpmClientHandler
import os
import sublime


PLATFORMS = {
    'windows': {
        'x64': '@rometools/cli-win32-x64/rome.exe',
        'arm64': '@rometools/cli-win32-arm64/rome.exe',
    },
    'osx': {
        'x64': '@rometools/cli-darwin-x64/rome',
        'arm64': '@rometools/cli-darwin-arm64/rome',
    },
    'linux': {
        'x64': '@rometools/cli-linux-x64/rome',
        'arm64': '@rometools/cli-linux-arm64/rome',
    },
}


def resolve_platform_binary() -> Optional[str]:
    return PLATFORMS.get(sublime.platform(), {}).get(sublime.arch())


class LspRomePlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'node_modules', resolve_platform_binary() or '')

    @classmethod
    def is_allowed_to_start(
        cls,
        window: sublime.Window,
        initiating_view: Optional[sublime.View] = None,
        workspace_folders: Optional[List[WorkspaceFolder]] = None,
        configuration: Optional[ClientConfig] = None
    ) -> Optional[str]:
        if not resolve_platform_binary():
            return 'LSP-rome does not support your platform currently.'
        return None


def plugin_loaded() -> None:
    LspRomePlugin.setup()


def plugin_unloaded() -> None:
    LspRomePlugin.cleanup()
