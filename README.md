# CyberLab CLI



## 1. 🎯Project Goal


CyberLab CLI is a powerful automation layer built on top of ```VBoxManage```, designed to streamline the deployment and 
management of cyber lab (virtual training environment). It eliminates manual steps by providing:

### 🔧 Core Automation Features
- **One-command OVA deployment:** 
Download and import pre-configured virtual machine templates that simulate a real corporate network from remote repositories.

- **Bulk operations:**
Start/stop/reset an entire cyber lab (multiple VMs) with a single CLI command.

- **Consistency:**
Ensure identical lab environments across teams via version-controlled OVA imports.

### 🚩 Use Cases
- **Cybersecurity training:** Rapidly deploy vulnerable VMs for pentesting practice.

- **Research/Development:** Test exploits in isolated, reproducible environments.



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

**Install Virtual Machines**   
Download and import VMs (skip fetching OVA files if `--skip-fetching` is set):
```bash
python cyberlab.py install [--skip-fetching]
```
* Without `--skip-fetching`: Downloads OVA files before importing.
* With `--skip-fetching`: Imports only (assumes OVA files already present).  

**Start the Cyber Lab**  
Launch all configured VMs:  
```bash
python cyberlab.py startup
```

**Stop the Cyber Lab**  
Gracefully shut down all VMs:
```bash
python cyberlab.py shutdown
```

### ⚙️ Configuration
The tool uses the current working directory (`cwd`) to:
1. Look for the config file (`config.yaml`).
2. Store files by default in:
   - OVA files: `./ova/`
   - -Virtual machines: `./vms/`

To customize paths, modify these settings in `config.yaml` file:
```yaml
storage:
  ova: 
    store_to: /custom/path/for/ova_files
  virtual_machines:
    store_to: /custom/path/for/vms
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
pyinstaller --onefile --name=cyberlab --workpath=./tmp --specpath=./tmp cyberlab.py
```

### 🤔 What This Command Does

| Option           | Purpose                                                                     |
|------------------|-----------------------------------------------------------------------------|
| --onefile        | Packages everything into a single executable (no separate dependency files) |
| --name=cyberlab  | Sets the output filename (`cyberlab` or `cyberlab.exe`)                     |
| --workpath=./tmp | Stores temporary build files in `./tmp`                                     |
| --specpath=./tmp | Places PyInstaller's `.spec` configuration file in `./tmp`                  |
| cyberlab.py      | Source script to package                                                    |

### 📂 Output Files
* The executable will be in `./dist/`:
    - **Windows:** `dist/cyberlab.exe`
    - **Linux/macOS:** `dist/cyberlab`
* Temporary files (`./tmp`) can be deleted after building:
```bash
rm -rf ./tmp  # Linux/macOS
rmdir /s /q tmp  # Windows (CMD)
```

### 🚀 How to Run the Executable
Windows:
```powershell
.\dist\cyberlab.exe [command] [arguments]
```
Linux/macOS:
```bash
chmod +x ./dist/cyberlab  # Make executable
./dist/cyberlab [command] [arguments]
```

### ⚠️ Important Notes
1. Platform-Specific Builds
    - The executable is built for your current OS (Linux builds Linux binaries, Windows builds `.exe`).
    - For cross-platform distribution, build on each target platform.
2. File size
    - The resulting binary may be large (10-50MB) as it embeds Python and dependencies.
3. No Python Required
    - The executable runs independently - no Python installation needed on target machines.
4. Configuration Files
    - Cyber Lab CLI uses current working directory (`cwd`) to look for config file (`config.yaml`)



## 7. 📜 License 

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Key Permissions
✅ Free to use, modify, and distribute  
✅ Permitted for commercial use  
✅ No liability or warranty

### You must include:
- The original copyright notice (`Copyright (c) 2025 Mikalai Viarbila (github.com/nickolay3132)`)
- A copy of the license text