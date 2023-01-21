from LSP.plugin import ClientConfig, WorkspaceFolder
from LSP.plugin.core.typing import Dict, List, Optional
from lsp_utils import NpmClientHandler
import json
import os
import sublime


PLATFORMS = {
    'windows': {
        'x64': {
            'binary': '@rometools/cli-win32-x64/rome.exe',
            'package': '@rometools/cli-win32-x64'
        },
        'arm64': {
            'binary': '@rometools/cli-win32-arm64/rome.exe',
            'package': '@rometools/cli-win32-arm64'
        },
    },
    'osx': {
        'x64': {
            'binary': '@rometools/cli-darwin-x64/rome',
            'package': '@rometools/cli-darwin-x64'
        },
        'arm64': {
            'binary': '@rometools/cli-darwin-arm64/rome',
            'package': '@rometools/cli-darwin-arm64'
        },
    },
    'linux': {
        'x64': {
            'binary': '@rometools/cli-linux-x64/rome',
            'package': '@rometools/cli-linux-x64'
        },
        'arm64': {
            'binary': '@rometools/cli-linux-arm64/rome',
            'package': '@rometools/cli-linux-arm64'
        },
    },
}

RESOLVED_PLATFORM = PLATFORMS.get(sublime.platform(), {}).get(sublime.arch(), {})  # type: Optional[Dict[str, str]]

def resolve_platform_binary() -> Optional[str]:
    return RESOLVED_PLATFORM.get('binary') if RESOLVED_PLATFORM else None


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
        if not RESOLVED_PLATFORM:
            return
        package_name = RESOLVED_PLATFORM['package']
        package_json = os.path.join(package_name, 'package.json');
        binary_name = os.path.join(package_name, ('rome.exe' if 'win32' in package_name else 'rome'))
        for folder in workspace_folders:
            package_json_path = os.path.join(folder.path, 'node_modules', package_json)
            binary_path = os.path.join(folder.path, 'node_modules', binary_name)
            if not os.path.isfile(package_json_path) or not os.path.isfile(binary_path):
                continue
            try:
                with open(package_json_path , 'r') as fp:
                    version = json.loads(fp.read())['version']
                    # Ignore versions lower than 0.9.0 as those didn't embed LSP server.
                    version_tuple = tuple(map(int, (version.split('.'))))
                    if len(version_tuple) == 3 and version_tuple < (0, 9, 0):
                        continue
                return binary_path
            except:
                continue
        return None


def plugin_loaded() -> None:
    LspRomePlugin.setup()


def plugin_unloaded() -> None:
    LspRomePlugin.cleanup()
