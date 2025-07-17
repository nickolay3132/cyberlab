# CyberLab Management Tool



## 1. 🎯Project Goal


CyberLab Management Tool is a powerful automation layer built on top of VBoxManage, designed to streamline the 
deployment and management of CyberLab — a virtual training environment tailored for cybersecurity labs and 
experimentation. It eliminates manual steps by providing:

### 🔧 Core Automation Features
- One-command OVA deployment: Download and import pre-configured virtual machine templates that simulate a real 
corporate network from remote repositories.
- Bulk operations: Start/stop/reset an entire CyberLab (multiple VMs) with a single CLI command.
- Consistency: Ensure identical lab environments across teams via version-controlled OVA imports.

### 🧭 Interface Options
CyberLab is available in two flavors:
- cyberlab_cli: A command-line interface (CLI) that exposes the full power of VBoxManage-backed automation. Perfect 
for scripting, integration into CI pipelines, and experienced operators.
- cyberlab (GUI): A graphical user interface that simplifies usage and makes CyberLab accessible to non-technical 
users. Under the hood, it wraps and delegates tasks to the CLI component — providing visual interaction with CLI features.

✅ The GUI version is built directly atop the CLI, ensuring consistent behavior and compatibility across both modes of operation.

### 🚩 Use Cases
Cybersecurity training: Rapidly deploy vulnerable VMs for pentesting practice.

Research/Development: Test exploits in isolated, reproducible environments.



## 2. 🖥️ System Requirements


Minimum
- **RAM:** 8 GB
- **CPU:** 4 cores / 8 threads
- **Storage:** 70 GB free space or more
- **OS:** 64-bit Windows/Linux/macOS with VirtualBox 6.0+

Optimal (Recommended)
- **RAM:** 16 GB
- **CPU:** 6 cores / 12 threads
- **Storage:** 80 GB free space or more
- **Virtualization:** VT-x/AMD-V enabled in BIOS for better performance



## 3. ⚙️ Dependencies


Before using CyberLab CLI, ensure your system meets these requirements:

- [VirtualBox](https://www.virtualbox.org/) 6.x or 7.x
- `VBoxManage` in your `PATH` (verify with `VBoxManage --version`).
- [Python](https://www.python.org/) 3.8 or newer (check with `python --version`).

### 🛠️ Troubleshooting
- `VBoxManage` not found? Add VirtualBox to your `PATH`:
    * **Linux/macOS:** Add `export PATH=$PATH:/usr/lib/virtualbox` to `~/.bashrc`.
    * **Windows:** Include VirtualBox's install dir (e.g., C:\Program Files\Oracle\VirtualBox) in system `PATH`.
- **Python version mismatch?** Use `python3` explicitly or update via `pyenv`.



## 4. 📥 Installation Guide (Windows & Linux)


This guide covers the installation process for both Windows and Linux (Ubuntu/Debian-based).
### Clone the Repository
```bash
git clone https://github.com/nickolay3132/cyberlab.git
cd cyberlab
```

### Create & Activate a Virtual Environment
🐧 Linux (Ubuntu/Debian-based)
```bash
python3 -m venv .venv          # Create virtual environment
source .venv/bin/activate      # Activate it
```

🪟 Windows (PowerShell)
```powershell
python -m venv .venv         # Create virtual environment
.venv\Scripts\activate       # Activate it (PowerShell)
```

### Install Dependencies
🐧 Linux / 🪟 Windows (Same Command)
```bash
pip install --upgrade pip
pip install -r requirements.txt  # Install dependencies
```

### Run the Project
🐧 Linux / 🪟 Windows (Same Command)
```bash
python cyberlab.py  # See available commands
```



## 5. 🚀 Usage 

### 😊 Basic Commands   
**Run the tool with:**
```bash
python cyberlab.py [COMMAND] [OPTIONS]
```
---

**Install Virtual Machines**   
Download and import VMs from OVA files:
```bash
python cyberlab.py install [--skip-download] [--no-verify]
```
* **Without flags**: Downloads OVA files (if missing) and verifies their integrity before import.
* `--skip-download`: Skips downloading OVA files (assumes files are already present locally). 
* `--no-verify`: Skips hash verification for existing OVA files (faster but less secure).
---

**Start the CyberLab**  
Launch all configured VMs:  
```bash
python cyberlab.py startup
```
---

**Stop the CyberLab**  
Gracefully shut down all VMs:
```bash
python cyberlab.py shutdown [--force]
```
* **Without flags:** Graceful shutdown (sends ACPI power-off signal to VMs).
* `--force`: Force immediate shutdown of all VMs (equivalent to pulling the power).
---

### 📸 Manage CyberLab Snapshots
Snapshots preserve the entire VM state (disk, memory, settings) for easy rollback.   
#### **Usage:**
```bash
python cyberlab.py snapshot <command> [options]
```
---
**Subcommands:**

**Create snapshot**   
Save current state of all VMs.
```bash
python cyberlab.py snapshot create -n <NAME> [-d <DESCRIPTION>]
```
| Short | Long            | Description                                   | Required |
|-------|-----------------|-----------------------------------------------|----------|
| `-n`  | `--name`        | Snapshot name (non-unique allowed)            | Yes      |
| `-d`  | `--description` | Contextual details (e.g., "Pre-update state") | No       |
---

**List Snapshots**   
Display all available snapshots with their metadata.
```bash
python cyberlab.py snapshot list 
```
---

**Restore Snapshot**   
Roll back all VMs to a previously saved state.
```bash
python cyberlab.py snapshot restore -n <NAME>
```
| Short | Long     | Description                     | Required |
|-------|----------|---------------------------------|----------|
| `-n`  | `--name` | Name of the snapshot to restore | Yes      |

[//]: # (---)

[//]: # ()
[//]: # (**Delete Snapshot**   )

[//]: # (Remove a snapshot &#40;⚠️ child snapshots will be deleted recursively&#41;.)

[//]: # (```bash)

[//]: # (python cyberlab.py snapshot delete [-h] [--all] [-n NAME])

[//]: # (```)

[//]: # (| Short | Long     | Description              | Required |)

[//]: # (|-------|----------|--------------------------|----------|)

[//]: # (| `-n`  | `--name` | Delete specific snapshot | No*      |)

[//]: # (|       | `--all`  | Delete ALL snapshots     | No*      |)

[//]: # ()
[//]: # (> *Either `--name` or `--all` must be specified)

### ⚙️ Configuration
The tool uses the current working directory (`cwd`) to:
1. Look for the config file (`config.yaml`).
2. Store files by default in:
   - OVA files: `./ova/`
   - Virtual machines: `./vms/`
   - Import Log: `./import_log/`

To customize paths, modify these settings in `config.yaml` file:
```yaml
storage:
  ova_store_to: /custom/path/for/ova_files
  vms_store_to: /custom/path/for/vms
  import_log_store_to: /custom/path/for/import_log
```

### 📚 Help & Documentation
For detailed command help, use:
```bash
python cyberlab.py --help          # General help
python cyberlab.py install --help  # Command-specific help
```



## 6. 🔧 Cross-platform packaging


To package `cyberlab.py` into a single executable file (`cyberlab.exe` on Windows or `cyberlab` on Linux/macOS) 
using PyInstaller, run the following command:
```bash
pip install pyinstaller
python build.py
```

### 📂 Output Files
* The executable will be in `./dist/`:
    - **Windows:** `dist/cyberlab.exe`
    - **Linux/macOS:** `dist/cyberlab`
* Temporary files (`./tmp`) can be deleted after building:
```bash
rm -rf ./tmp  # Linux/macOS
rmdir /s /q tmp  # Windows (CMD)
```

### 🚀 How to Run the Executables
CyberLab is distributed in two variants:
- CyberLab CLI: A command-line interface for automation and scripting.
- CyberLab GUI: A graphical user interface built on top of the CLI for visual interaction.

After building with PyInstaller, the executables will appear in the dist folder:

🪟 Windows:
```powershell
# Run CLI
.\dist\CyberLabCli.exe [command] [arguments]

# Run GUI
.\dist\CyberLab.exe
```

🐧 Linux / 🍎 macOS:
```bash
# Make both files executable
chmod +x ./dist/CyberLabCli
chmod +x ./dist/CyberLab

# Run CLI
./dist/CyberLabCli [command] [arguments]

# Run GUI
./dist/CyberLab
```


📌 The GUI wraps around the CLI — make sure both executables are present in the same directory so that GUI operations can invoke the CLI correctly.

### ⚠️ Important Notes
1. Platform-Specific Builds
    - The executable is built for your current OS (Linux builds Linux binaries, Windows builds `.exe`).
    - For cross-platform distribution, build on each target platform.
2. File size
    - The resulting binary may be large (10-50MB) as it embeds Python and dependencies.
3. No Python Required
    - The executable runs independently - no Python installation needed on target machines.
4. Configuration Files
    - CyberLab CLI uses current working directory (`cwd`) to look for config file (`config.yaml`)



## 7. 📜 License 

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Key Permissions
✅ Free to use, modify, and distribute  
✅ Permitted for commercial use  
✅ No liability or warranty

### You must include:
- The original copyright notice (`Copyright (c) 2025 Mikalai Viarbila (github.com/nickolay3132)`)
- A copy of the license text