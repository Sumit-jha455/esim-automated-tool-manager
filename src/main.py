from tool_manager import ToolManager
from version_checker import VersionChecker


def print_header():
    print()
    print("=" * 55)
    print("        eSim Automated Tool Manager")
    print("=" * 55)


def select_tool(manager):

    tools = manager.list_tools()

    print("\nAvailable Tools:")

    tool_keys = list(tools.keys())

    for index, key in enumerate(tool_keys, start=1):
        print(
            f"{index}. "
            f"{tools[key]['name']} - "
            f"{tools[key]['description']}"
        )

    try:
        choice = int(input("\nSelect tool: "))

        if choice < 1 or choice > len(tool_keys):
            print("Invalid selection.")
            return None

        return tool_keys[choice - 1]

    except ValueError:
        print("Please enter a valid number.")
        return None


def list_installed_tools(manager):

    print("\nInstalled Tool Status")
    print("-" * 55)

    for key in manager.list_tools():

        result = manager.check_tool(key)

        if result["installed"]:
            print(
                f"✓ {result['name']}: "
                f"{result['version']}"
            )
        else:
            print(
                f"✗ {result['name']}: "
                f"Not Installed"
            )


def check_version(manager):

    tool_key = select_tool(manager)

    if tool_key is None:
        return

    result = manager.check_tool(tool_key)

    print()

    if result["installed"]:
        print(f"✓ {result['name']} is installed.")
        print(f"Version: {result['version']}")
    else:
        print(
            f"✗ {result['name']} is not installed."
        )


def install_tool(manager):

    tool_key = select_tool(manager)

    if tool_key is None:
        return

    tool = manager.tools[tool_key]

    print(
        f"\nYou selected: {tool['name']}"
    )

    confirm = input(
        "Do you want to install it? (y/n): "
    ).lower()

    if confirm != "y":
        print("Installation cancelled.")
        return

    print("\nStarting installation...")

    success, message = manager.install_tool(tool_key)

    if success:
        print("\n✓ Installation completed.")
        print(message)
    else:
        print("\n✗ Installation failed.")
        print(message)


def check_dependencies(manager):

    print("\nDependency Status")
    print("-" * 55)

    results = manager.check_dependencies()

    for dependency, installed in results.items():

        if installed:
            print(
                f"✓ {dependency}: Installed"
            )
        else:
            print(
                f"✗ {dependency}: Missing"
            )


def main():

    manager = ToolManager()

    while True:

        print_header()

        print("\n1. List Installed Tools")
        print("2. Check Tool Version")
        print("3. Install Tool")
        print("4. Check Dependencies")
        print("5. Exit")

        choice = input(
            "\nEnter your choice: "
        ).strip()

        if choice == "1":
            list_installed_tools(manager)

        elif choice == "2":
            check_version(manager)

        elif choice == "3":
            install_tool(manager)

        elif choice == "4":
            check_dependencies(manager)

        elif choice == "5":
            print("\nThank you for using eSim Tool Manager.")
            break

        else:
            print("\nInvalid choice.")

        input(
            "\nPress Enter to continue..."
        )


if __name__ == "__main__":
    main()