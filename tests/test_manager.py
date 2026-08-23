import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from version_checker import VersionChecker
from dependency_checker import DependencyChecker


def test_python_is_available():

    result = VersionChecker.is_tool_installed(
        "python"
    )

    assert result is True


def test_python_dependency():

    result = DependencyChecker.check_dependency(
        "python"
    )

    assert result is True


if __name__ == "__main__":
    test_python_is_available()
    test_python_dependency()

    print("All tests passed.")