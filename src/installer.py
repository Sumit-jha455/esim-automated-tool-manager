import subprocess
import platform
import os

from logger import logger
from downloader import ToolDownloader


class ToolInstaller:

    @staticmethod
    def get_os():
        system = platform.system()

        if system == "Windows":
            return "windows"

        elif system == "Linux":
            return "linux"

        elif system == "Darwin":
            return "macos"

        return "unknown"

    @staticmethod
    def command_exists(command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            return result.returncode == 0

        except Exception:
            return False

    @staticmethod
    def install_tool(tool_config):

        os_type = ToolInstaller.get_os()

        # =====================================================
        # WINDOWS
        # =====================================================

        if os_type == "windows":

            windows_config = tool_config.get(
                "windows",
                {}
            )

            package_manager = windows_config.get(
                "package_manager",
                "winget"
            )

            package_id = windows_config.get(
                "package_id"
            )

            # Check WinGet
            if not ToolInstaller.command_exists(
                f"{package_manager} --version"
            ):

                message = (
                    "WinGet is not available "
                    "on this Windows system."
                )

                logger.error(message)

                return False, message

            # -------------------------------------------------
            # Search package first
            # -------------------------------------------------

            search_command = (
                f'{package_manager} search '
                f'"{tool_config["name"]}"'
            )

            logger.info(
                "Searching package using command: %s",
                search_command
            )

            try:

                search_result = subprocess.run(
                    search_command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                search_output = (
                    search_result.stdout.strip()
                    or search_result.stderr.strip()
                )

                # -------------------------------------------------
                # Package unavailable -> official fallback
                # -------------------------------------------------

                if (
                    search_result.returncode != 0
                    or "No package found" in search_output
                ):

                    fallback = windows_config.get(
                        "fallback"
                    )

                    if fallback == "official":

                        official_url = tool_config.get(
                            "official_url"
                        )

                        if not official_url:

                            message = (
                                "No official download URL "
                                "is configured for this tool."
                            )

                            logger.error(message)

                            return False, message

                        print(
                            "\nWinGet package not available."
                        )

                        print(
                            "Using official distribution "
                            "fallback..."
                        )

                        install_directory = os.path.join(
                            os.path.expanduser("~"),
                            "eSimTools",
                            tool_config["name"]
                        )

                        archive_name = (
                            "ngspice-47_64.7z"
                        )

                        success, result = (
                            ToolDownloader.download_and_extract(
                                official_url,
                                archive_name,
                                install_directory
                            )
                        )

                        if not success:

                            return False, result

                        return True, (
                            "Official package downloaded "
                            "and extracted successfully.\n"
                            f"Location: {result}"
                        )

                    message = (
                        f"{tool_config['name']} is not "
                        "available in the configured "
                        "WinGet source."
                    )

                    logger.warning(message)

                    return False, message

            except subprocess.TimeoutExpired:

                message = (
                    "Package search timed out."
                )

                logger.error(message)

                return False, message

            except Exception as error:

                logger.error(
                    "Package search failed: %s",
                    error
                )

                return False, str(error)

            # -------------------------------------------------
            # WinGet installation
            # -------------------------------------------------

            command = (
                f"{package_manager} install "
                f"--id {package_id} "
                "--exact "
                "--accept-source-agreements "
                "--accept-package-agreements"
            )

        # =====================================================
        # LINUX
        # =====================================================

        elif os_type == "linux":

            linux_config = tool_config.get(
                "linux",
                {}
            )

            package_manager = linux_config.get(
                "package_manager",
                "apt"
            )

            package_name = linux_config.get(
                "package_name"
            )

            if not ToolInstaller.command_exists(
                f"{package_manager} --version"
            ):

                message = (
                    f"Package manager "
                    f"'{package_manager}' "
                    "is not available."
                )

                logger.error(message)

                return False, message

            command = (
                f"sudo {package_manager} update && "
                f"sudo {package_manager} install "
                f"-y {package_name}"
            )

        # =====================================================
        # UNSUPPORTED OS
        # =====================================================

        else:

            message = (
                "Automatic installation is currently "
                "supported for Windows and Linux."
            )

            logger.error(message)

            return False, message

        # =====================================================
        # EXECUTE INSTALLATION
        # =====================================================

        logger.info(
            "Installing tool using command: %s",
            command
        )

        try:

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                output = (
                    result.stdout.strip()
                    or
                    "Installation completed successfully."
                )

                logger.info(
                    "Tool installation completed successfully."
                )

                return True, output

            error_message = (
                result.stderr.strip()
                or result.stdout.strip()
                or "Unknown package manager error."
            )

            logger.error(
                "Installation failed: %s",
                error_message
            )

            return False, error_message

        except Exception as error:

            logger.error(
                "Installation exception: %s",
                error
            )

            return False, str(error)