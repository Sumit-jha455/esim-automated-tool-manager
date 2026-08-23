import shutil

from logger import logger


class DependencyChecker:

    COMMON_DEPENDENCIES = [
        "python",
        "git"
    ]

    @staticmethod
    def check_dependency(dependency):
        executable = shutil.which(dependency)

        status = executable is not None

        logger.info(
            "Dependency check: %s -> %s",
            dependency,
            status
        )

        return status

    @staticmethod
    def check_all():
        results = {}

        for dependency in DependencyChecker.COMMON_DEPENDENCIES:
            results[dependency] = (
                DependencyChecker.check_dependency(dependency)
            )

        return results