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
- **Virtualization:** VT-x/AMD-V enabled in DIOS for better performance


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
### 1. Clone the Repository
```
git clone https://github.com/nickolay3132/cyberlab.git
cd your-repo  # Enter the project directory
```

### 2. Create & Activate a Virtual Environment
🐧 Linux (Ubuntu/Debian-based)
```
python3 -m venv venv          # Create virtual environment
source venv/bin/activate      # Activate it
```

🪟 Windows (PowerShell)
```
python -m venv venv           # Create virtual environment
.\venv\Scripts\activate       # Activate it (PowerShell)
```

### 3. Install Dependencies
🐧 Linux / 🪟 Windows (Same Command)
```
pip install --upgrade pip
pip install -r requirements.txt  # Install dependencies
```

### 4. Run the Project
🐧 Linux / 🪟 Windows (Same Command)
```
python cyberlab.py  # See available commands
```
## 5. 🚀 Usage 
## 6. 🔧 Cross-platform packaging
## 7. 📜 License 