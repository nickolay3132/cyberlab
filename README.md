CyberLab Management Tool
========================

----

## 1. 🎯Project Goal

Cyberlab Management Tool is an automation layer built on top of VBoxManage and VirtualBox, developed to
enable users to easily manage CyberLab - an environment made of virtual machines designed for 
cybersecurity training and experimentation. It provides the following features:

- **One-config-for-all!**
    Testing environments are easily deployed on many machines. The only requirements are Cyberlab Management
    Tool and configuration file.

- **Smooth workflow**
    Install, Start, Stop and make Snapshots of machines with a single click. No need to manually
    start every machine - just press a button.

- **Cloud integration**
    Don't want to carry hard drives with hunders of GB worth of OVAs? Just upload them to whatever cloud
    storage and provide the link in config file. Everything else will be handled by CyberLab Management Tool.

### Interface options

Cyberlab Management Tool is privded in two forms:

-   **GUI** which looks pretty (I hope) and provides everything you need for comfortable and efficient workflow.

-   **CLI** which is great for scripting (if you feel the need to automate it even further).

## 2. 🖥️ System Requirements

> NOTE: System requirements mentioned here are stated as such for the *CYBERPOLYGON*, not for the actual application :)
> Of course one python executable wouldn't need 8GB of RAM. But we still recommend using 64-bit system unless you have some really
> strong reason not to do so.

> NOTE 2: "Minimum" requirements may not be the *actual* minimum, but we *really* do**n't** recommend you deploying 6+ VMs
> on a computer which has 8GB of ram... Though, if you are indeed brave enough, please let us know what the real "minimum"
> required specs are.

**Minimum**

| Spec | Requirement |
| :-- | --: |
| RAM  | 8 GB               |
| CPU  | 4 Cores |
| Storage | +70GB Free |
| OS | 64-bit |
| VirtualBox | Version 6.0+ |

**Optimal (Recommended)**

| Spec | Requirement |
| :-- | --: |
| RAM | 16 GB |
| CPU | 6 cores |
| Storage |  +80GB Free |
| OS | 64-bit |
| Virtualization | **VT-X/AMD-V** enabled in *BIOS*



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



## 4. 📥 Installation Guide

### Linux

1. Clone the repository
``` bash
git clone https://github.com/nickolay3132/cyberlab.git && cd cyberlab
```

2. Create and activate virtual environment for Python.
```bash
python3 -m venv .venv && source .venv/bin/activate
```

3. Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Installation is complete! To run use:
```
python3 cyberlab.py # if python venv is activated
.venv/bin/python3 cyberlab.py # if python venv is not activated
```
---

### Windows

1. Clone the repository (if git is in `%PATH%`) or download and extract sources

    Using git:

    ```powershell
    git clone https://github.com/nickolay3132/cyberlab.git && cd cyberlab
    ```

    By downloading archive:

    ```powershell
    wget https://github.com/nickolay3132/cyberlab/archive/refs/heads/gui.zip -OutFile CLMT.zip
    Expand-Archive -Path CLMT.zip -DestinationPath CyberLab
    cd CyberLab
    ```

2. Create and activate python virtual environment
```powershell
python -m venv .venv
.venv\Scripts\Activate
```

3. Install Pyton dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Installation is complete! To run use:
```
python cyberlab.py
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
| Short | Long              | Description                                                             | Required |
|-------|-------------------|-------------------------------------------------------------------------|----------|
|       | `--skip-download` | Skips downloading OVA files (assumes files are already present locally) | No       | 
|       | `--no-verify`     | Skips hash verification for existing OVA files (faster but less secure) | No       |
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
| Short | Long      | Description                                                           | Required |
|-------|-----------|-----------------------------------------------------------------------|----------|
|       | `--force` | Force immediate shutdown of all VMs (equivalent to pulling the power) | No       |

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


### ⚙️ Configuration
The tool uses the current working directory (`cwd`) to look for the config file (`config.yaml`).

To customize storage paths, modify these settings in `config.yaml` file:
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
    - **Windows:** `dist\CyberLab.exe` and `dist\CyberLabCli.exe`
    - **Linux/macOS:** `dist/CyberLab` and `dist/CyberLabCli`

> NOTE: To remove temporary build files, enter `y` when prompted if you
> wnat to delete them.

> NOTE 2: Cyberlab uses searches only current working directory (`cwd`) for config file (`config.yaml`)

## 7. 📜 License 

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Key Permissions
✅ Free to use, modify, and distribute  
✅ Permitted for commercial use  
✅ No liability or warranty

### You must include:
- The original copyright notice (`Copyright (c) 2025 Mikalai Viarbila (github.com/nickolay3132)`)
- A copy of the license text
