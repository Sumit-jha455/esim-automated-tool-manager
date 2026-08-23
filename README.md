# eSim Automated Tool Manager

**Python | Command-Line Interface | eSim | FOSSEE Internship Screening Task 5**

A Python-based command-line tool manager designed to automate the management of external tools and dependencies used with eSim.

---

## 📌 Screening Task

**FOSSEE Semester Long Internship — Autumn 2026**

**Task 5: Tool Manager (CSE and related fields)**

---

## 📖 Overview

eSim is an open-source Electronic Design Automation (EDA) tool that integrates several external tools and libraries for circuit design, simulation, analysis, and PCB-related workflows.

Managing these external tools manually can be time-consuming and may lead to issues such as missing dependencies, incompatible versions, or incorrect installation paths.

The **eSim Automated Tool Manager** provides a centralized command-line interface for detecting, installing, verifying, and managing external tools.

The current prototype demonstrates automated management of **Ngspice** and configuration support for **KiCad**.

---

## 🎯 Objectives

The main objectives of the project are:

- Automate external tool installation.
- Detect installed tools.
- Check tool versions.
- Check required dependencies.
- Provide an easy-to-use command-line interface.
- Provide an official-source fallback when a package is unavailable.
- Automatically download and extract supported tool packages.
- Verify successful installation.
- Maintain logs of important operations and errors.
- Provide a modular architecture for future extensions.

---

## ✨ Features

### Tool Management

- List installed tools.
- Check tool installation status.
- Check installed tool versions.
- Install supported tools.

### Automated Installation

- Detect the operating system.
- Check package manager availability.
- Check package availability.
- Use an official distribution fallback when required.
- Automatically download supported packages.
- Automatically extract `.7z` archives.
- Discover installed executables.
- Verify installation after extraction.

### Dependency Checking

Currently checks:

- Python
- Git

### User Interface

The application provides a simple command-line interface:

```text
===================================================
            eSim Automated Tool Manager
===================================================

1. List Installed Tools
2. Check Tool Version
3. Install Tool
4. Check Dependencies
5. Exit
```

### Logging

Important operations such as installation attempts, executable discovery, dependency checks, version checks, and errors are recorded using the project's logging system.

---

## 🛠️ Technology Stack

| Technology | Purpose |
| Python | Core implementation |
| JSON | Tool configuration |
| `subprocess` | System command execution |
| `shutil` | Executable detection |
| `platform` | Operating system detection |
| `py7zr` | `.7z` archive extraction |
| Git | Version control |
| PowerShell / WinGet | Windows package management |

---

## 🏗️ System Architecture

```text
                    +----------------------+
                    |    CLI Interface     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Tool Manager      |
                    +----------+-----------+
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
       +-------------+  +-------------+  +-------------+
       |  Installer  |  |   Version   |  | Dependency  |
       |             |  |   Checker   |  |   Checker   |
       +------+------+  +-------------+  +-------------+
              |
              v
       +-------------+
       |  Downloader |
       +------+------+
              |
              v
       +----------------------+
       |    External Tools    |
       |    Ngspice / KiCad   |
       +----------------------+
```

The architecture is modular so that additional tools and management capabilities can be added without significantly changing the existing components.

---

## 📂 Project Structure

```text
esim-automated-tool-manager/
│
├── config/
│   └── tools.json
│
├── docs/
│   └── Design_Document.pdf
│
├── logs/
│
├── screenshots/
│
├── src/
│   ├── main.py
│   ├── tool_manager.py
│   ├── installer.py
│   ├── downloader.py
│   ├── version_checker.py
│   ├── dependency_checker.py
│   └── logger.py
│
├── tests/
│   └── test_manager.py
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## ⚙️ Requirements

Before running the project, make sure the following are available:

- Python 3.10 or later
- Git
- Internet connection for downloading external tools
- Windows or Linux operating system

For Windows, WinGet availability is checked automatically when applicable.

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
```

### 2. Navigate to the project

```bash
cd esim-automated-tool-manager
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Application

From the project root:

```bash
python src/main.py
```

The application displays:

```text
===================================================
            eSim Automated Tool Manager
===================================================

1. List Installed Tools
2. Check Tool Version
3. Install Tool
4. Check Dependencies
5. Exit
```

---

## 🔧 Ngspice Installation Workflow

The current prototype demonstrates the Ngspice installation workflow on Windows.

### Step 1 — Check Package Manager

The application checks whether WinGet is available.

### Step 2 — Check Package Availability

The application checks whether Ngspice is available through the configured WinGet source.

### Step 3 — Official Fallback

If Ngspice is unavailable through WinGet, the manager uses the configured official Ngspice distribution as a fallback.

### Step 4 — Download

The Ngspice package is downloaded automatically.

### Step 5 — Extraction

The downloaded `.7z` archive is extracted using `py7zr`.

### Step 6 — Executable Discovery

The manager recursively searches the installation directory for:

```text
ngspice_con.exe
```

### Step 7 — Installation Verification

The discovered executable is used to verify the installed Ngspice installation.

The demonstrated installation was successfully verified as:

```text
Ngspice 47
```

---

## 🔍 Dependency Checking

Select:

```text
4. Check Dependencies
```

The application checks essential dependencies.

Currently checked dependencies:

- Python
- Git

Example output:

```text
Dependency Status
----------------------------------------
✓ python: Installed
✓ git: Installed
```

---

## 🧪 Testing

The project includes automated tests for the core tool manager functionality.

Run:

```bash
python tests/test_manager.py
```

Expected result:

```text
All tests passed.
```

### Python Syntax Validation

Individual source files can also be syntax-checked using:

```bash
python -m py_compile src/main.py
python -m py_compile src/tool_manager.py
python -m py_compile src/installer.py
python -m py_compile src/downloader.py
python -m py_compile src/version_checker.py
python -m py_compile src/dependency_checker.py
```

---

## 📸 Screenshots

Demonstration screenshots are available in the `screenshots/` directory.

The screenshots demonstrate:

- Main CLI interface
- Installed tool detection
- Dependency checking
- Ngspice installation
- Official-source fallback
- Ngspice executable discovery
- Version verification
- Automated test execution

---

## 📋 Requirement Coverage

| Requirement | Status |
| Tool Installation Management | ✅ Implemented |
| Update and Upgrade System | 🔄 Future Enhancement |
| Configuration Handling | 🟡 Partially Implemented |
| Dependency Checker | ✅ Implemented |
| User Interface | ✅ Implemented |
| Additional Features | 🟡 Partial / Future |

The detailed requirement coverage matrix is available in the Design Document.

---

## ⚠️ Current Limitations

The current proof-of-concept has the following limitations:

- Automatic update and upgrade functionality is not implemented.
- Complete GUI support is not implemented.
- macOS installation support is not implemented.
- The complete automatic installation workflow is demonstrated primarily with Ngspice.
- Full automatic PATH/environment configuration is not implemented.
- The dependency checker currently covers a limited set of dependencies.

---

## 🚀 Future Enhancements

Future versions can include:

- Automatic tool update detection.
- Automatic upgrade functionality.
- Version compatibility management.
- SHA-256/checksum verification.
- Tool uninstall and rollback.
- Automatic PATH configuration.
- GUI using Tkinter or PyQt.
- macOS support.
- Chocolatey and Homebrew integration.
- Additional eSim external tools and dependencies.
- Expanded automated testing.
- Detailed diagnostic reports.

---

## 📄 Documentation

The detailed technical design document is available at:

```text
docs/eSim_Automated_Tool_Manager_Design_Document.pdf
```

The document contains:

- Problem Statement
- Objectives
- System Architecture
- Module Breakdown
- Installation Workflow
- Version Checking
- Dependency Checking
- Configuration Design
- Testing and Validation
- Limitations
- Future Enhancements
- Requirement Coverage Matrix

---

## 👨‍💻 Submitted By:

**Sumit Kumar Jha**

B.Tech — Computer Science & Engineering  
Dronacharya Group of Institutions  
Dr. A.P.J. Abdul Kalam Technical University (AKTU)

---

## 📌 Disclaimer

This project is a proof-of-concept developed as part of the **FOSSEE Semester Long Internship — Autumn 2026** screening task.

The implementation clearly distinguishes currently implemented functionality from planned future enhancements.
