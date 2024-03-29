from LSP.plugin import ClientConfig, Response, WorkspaceFolder
from LSP.plugin.core.protocol import InitializeResult
from LSP.plugin.core.typing import List, Optional
from lsp_utils import NpmClientHandler
import json
import os
import sublime


PACKAGE_NAMES = {
    'windows': {
        'x64': '@rometools/cli-win32-x64',
        'arm64': '@rometools/cli-win32-arm64',
    },
    'osx': {
        'x64': '@rometools/cli-darwin-x64',
        'arm64': '@rometools/cli-darwin-arm64',
    },
    'linux': {
        'x64': '@rometools/cli-linux-x64',
        'arm64': '@rometools/cli-linux-arm64',
    },
}

RESOLVED_PACKAGE_NAME = PACKAGE_NAMES.get(sublime.platform(), {}).get(sublime.arch())  # type: Optional[str]


def resolve_platform_binary() -> Optional[str]:
    if not RESOLVED_PACKAGE_NAME:
        return None
    return os.path.join(RESOLVED_PACKAGE_NAME, ('rome.exe' if sublime.platform() == 'windows' else 'rome'))


class LspRomePlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'node_modules', resolve_platform_binary() or '')

    @classmethod
    def is_allowed_to_start(
        cls,
        window: sublime.Window,
        initiating_view: sublime.View,
        workspace_folders: List[WorkspaceFolder],
        configuration: ClientConfig
    ) -> Optional[str]:
        if not resolve_platform_binary():
            return 'LSP-rome does not support your platform currently.'
        rome_path = cls._resolve_rome_path(workspace_folders, configuration)
        if not rome_path:
            return 'LSP-rome could not resolve specified rome binary.'
        configuration.command = [rome_path, 'lsp-proxy']
        return None

    @classmethod
    def _resolve_rome_path(cls, workspace_folders: List[WorkspaceFolder], configuration: ClientConfig) -> Optional[str]:
        rome_lsp_bin = configuration.settings.get('rome.lspBin')
        if isinstance(rome_lsp_bin, str) and rome_lsp_bin:
            return cls._get_workspace_relative_path(rome_lsp_bin, workspace_folders)
        return cls._get_workspace_dependency(workspace_folders) or '${server_path}'

    @classmethod
    def _get_workspace_relative_path(cls, rome_lsp_bin: str, workspace_folders: List[WorkspaceFolder]) -> Optional[str]:
        if os.path.isabs(rome_lsp_bin):
            return rome_lsp_bin
        for folder in workspace_folders:
            possible_path = os.path.join(folder.path, rome_lsp_bin)
            if os.path.isfile(possible_path):
                return possible_path
        return None

    @classmethod
    def _get_workspace_dependency(cls, workspace_folders: List[WorkspaceFolder]) -> Optional[str]:
        binary_name = resolve_platform_binary()
        if not RESOLVED_PACKAGE_NAME or not binary_name:
            return
        package_json = os.path.join(RESOLVED_PACKAGE_NAME, 'package.json')
        for folder in workspace_folders:
            package_json_path = os.path.join(folder.path, 'node_modules', package_json)
            binary_path = os.path.join(folder.path, 'node_modules', binary_name)
            if not os.path.isfile(package_json_path) or not os.path.isfile(binary_path):
                continue
            try:
                with open(package_json_path, 'r') as fp:
                    version = json.loads(fp.read())['version']
                    # Ignore versions lower than 0.9.0 as those didn't embed LSP server.
                    version_tuple = tuple(map(int, (version.split('.'))))
                    if len(version_tuple) == 3 and version_tuple < (0, 9, 0):
                        continue
                return binary_path
            except Exception:
                continue
        return None

    def on_server_response_async(self, method: str, response: Response) -> None:
        if method == 'initialize':
            result = response.result  # type: InitializeResult
            version = result.get('serverInfo', {}).get('version')
            if version:
                session = self.weaksession()
                if session:
                    session.set_config_status_async(version)


def plugin_loaded() -> None:
    LspRomePlugin.setup()


def plugin_unloaded() -> None:
    LspRomePlugin.cleanup()
