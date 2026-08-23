import subprocess
import shutil
import platform
import os

from logger import logger


class VersionChecker:

    @staticmethod
    def is_tool_installed(command):
        """Check whether a command exists in the system PATH."""

        # Get executable name from command
        executable = command.split()[0].strip('"')

        exists = shutil.which(executable) is not None

        logger.info(
            "Checking installation status of %s: %s",
            executable,
            exists
        )

        return exists

    @staticmethod
    def find_executable(search_root, executable_name):
        """
        Recursively search for an executable inside
        the specified installation directory.

        This is especially useful for tools such as
        Ngspice that may be extracted into nested
        directories.
        """

        # Expand environment variables such as %USERPROFILE%
        search_root = os.path.expandvars(search_root)

        # Expand ~ if used in the path
        search_root = os.path.expanduser(search_root)

        # Convert to absolute path
        search_root = os.path.abspath(search_root)

        logger.info(
            "Searching for %s inside %s",
            executable_name,
            search_root
        )

        # Check whether installation directory exists
        if not os.path.isdir(search_root):

            logger.warning(
                "Installation directory does not exist: %s",
                search_root
            )

            return None

        # Case-insensitive comparison for Windows
        target_executable = executable_name.lower()

        # Search recursively
        for root, directories, files in os.walk(search_root):

            for filename in files:

                if filename.lower() == target_executable:

                    executable_path = os.path.abspath(
                        os.path.join(
                            root,
                            filename
                        )
                    )

                    logger.info(
                        "Executable found: %s",
                        executable_path
                    )

                    return executable_path

        logger.warning(
            "Executable not found: %s",
            executable_name
        )

        return None

    @staticmethod
    def get_version(command):
        """
        Execute a tool version command and return
        the version information.
        """

        try:

            logger.info(
                "Running version command: %s",
                command
            )

            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            # Combine stdout and stderr because some
            # command-line applications print version
            # information to stderr.
            output = (
                result.stdout.strip()
                or result.stderr.strip()
            )

            logger.info(
                "Version check result: %s",
                output
            )

            if result.returncode == 0:

                return output

            return (
                output
                or "Version check failed."
            )

        except subprocess.TimeoutExpired:

            logger.error(
                "Version check timed out: %s",
                command
            )

            return "Version check timed out."

        except Exception as error:

            logger.error(
                "Version check failed: %s",
                error
            )

            return f"Error: {error}"

    @staticmethod
    def get_os():
        """
        Detect the operating system.
        """

        system = platform.system()

        if system == "Windows":
            return "windows"

        if system == "Linux":
            return "linux"

        if system == "Darwin":
            return "macos"

        return "unknown"