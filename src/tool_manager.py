import json
import os
import platform

from version_checker import VersionChecker
from installer import ToolInstaller
from dependency_checker import DependencyChecker
from logger import logger


class ToolManager:

    def __init__(self):

        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "config",
            "tools.json"
        )

        with open(
            config_path,
            "r",
            encoding="utf-8"
        ) as file:

            self.tools = json.load(file)

        logger.info(
            "Tool Manager initialized."
        )

    def list_tools(self):
        return self.tools

    def check_tool(self, tool_key):

        if tool_key not in self.tools:
            return None

        tool = self.tools[tool_key]

        os_type = platform.system()

        # -------------------------------------------------
        # Windows: Search managed installation directory
        # -------------------------------------------------

        if os_type == "Windows":

            windows_config = tool.get(
                "windows",
                {}
            )

            executable_name = windows_config.get(
                "executable"
            )

            install_root = windows_config.get(
                "install_root"
            )

            if executable_name and install_root:

                executable_path = (
                    VersionChecker.find_executable(
                        install_root,
                        executable_name
                    )
                )

                if executable_path:

                    version_command = (
                        f'"{executable_path}" -v'
                    )

                    version = (
                        VersionChecker.get_version(
                            version_command
                        )
                    )

                    return {
                        "name": tool["name"],
                        "installed": True,
                        "version": version,
                        "path": executable_path
                    }

        # -------------------------------------------------
        # Normal PATH based detection
        # -------------------------------------------------

        version_command = tool[
            "version_command"
        ]

        installed = (
            VersionChecker.is_tool_installed(
                version_command
            )
        )

        if not installed:

            return {
                "name": tool["name"],
                "installed": False,
                "version": None
            }

        version = (
            VersionChecker.get_version(
                version_command
            )
        )

        return {
            "name": tool["name"],
            "installed": True,
            "version": version
        }

    def install_tool(self, tool_key):

        if tool_key not in self.tools:

            return (
                False,
                "Tool not found."
            )

        success, message = (
            ToolInstaller.install_tool(
                self.tools[tool_key]
            )
        )

        # -------------------------------------------------
        # Verify installation after successful installation
        # -------------------------------------------------

        if success:

            verification = (
                self.check_tool(tool_key)
            )

            if verification and verification["installed"]:

                logger.info(
                    "Installation verified for %s",
                    verification["name"]
                )

                return True, (
                    f"{message}\n\n"
                    "Installation verification:\n"
                    f"✓ {verification['name']} detected\n"
                    f"✓ Version: {verification['version']}\n"
                    f"✓ Installation verified"
                )

            logger.warning(
                "Installation completed but verification failed."
            )

            return True, (
                f"{message}\n\n"
                "⚠ Installation completed, "
                "but automatic verification failed."
            )

        return False, message

    def check_dependencies(self):

        return DependencyChecker.check_all()