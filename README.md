# CyberLab CLI

---

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

## 2. ⚙️ Dependencies
Before using CyberLab CLI, ensure your system meets these requirements:

- [VirtualBox](https://www.virtualbox.org/) 6.x or 7.x
- `VBoxManage` in your `PATH` (verify with `VBoxManage --version`).
- [Python](https://www.python.org/) 3.8 or newer (check with `python --version`).

### 🛠️ Verification
Run these commands to check your setup:
```bash
# Check VirtualBox:  
VBoxManage --version  

# Check Python:  
python --version  

# Install Python libs:  
python -m venv .venv
pip install -r requirements.txt
```

### Troubleshooting
- `VBoxManage` not found? Add VirtualBox to your `PATH`:
    * **Linux/macOS:** Add `export PATH=$PATH:/usr/lib/virtualbox` to `~/.bashrc`.
    * **Windows:** Include VirtualBox's install dir (e.g., C:\Program Files\Oracle\VirtualBox) in system `PATH`.
- **Python version mismatch?** Use `python3` explicitly or update via `pyenv`.

## 3. 📥 Installation
## 4. 🚀 Usage 
## 5. 🔧 Cross-platform packaging
## 6. 📜 License 