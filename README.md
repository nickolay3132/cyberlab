# CyberLab Management Tool (CLMT)

## 1. 🎯 Project Goal

CyberLab Management Tool (CLMT) is a powerful automation layer built on top of VBoxManage, designed to streamline the deployment and management of CyberLab — a virtual training environment tailored for cybersecurity labs and experimentation.

CLMT provides:

### 🔧 Core Automation Features
- One-command OVA deployment: Download and import pre-configured virtual machine templates that simulate a real corporate network.
- Bulk operations: Start, stop, or reset an entire CyberLab (multiple VMs) with a single CLI command.
- Consistency: Ensure identical lab environments across teams via version-controlled OVA imports.

### 🧭 Unified Interface

CLMT offers a unified entry point for both:

- **CLI**: Access full functionality via `clmt.py cli ...` commands.
- **GUI**: Launch a graphical interface with `clmt.py` for visual interaction.

✅ Both CLI and GUI are bundled into a single script (`clmt.py`) or binary (`clmt` / `clmt.exe`), ensuring consistent behavior across modes.

### 🚩 Use Cases
- Cybersecurity training: Rapidly deploy vulnerable VMs for pentesting practice.
- Research/Development: Test exploits in isolated, reproducible environments.

---

## 2. 🖥️ System Requirements

| Requirement     | Minimum                  | Recommended              |
|----------------|--------------------------|--------------------------|
| RAM            | 8 GB                     | 16 GB                    |
| CPU            | 4 cores / 8 threads      | 6 cores / 12 threads     |
| Storage        | 70 GB free               | 80 GB+ free              |
| OS             | 64-bit Windows/Linux/macOS |                          |
| VirtualBox     | 6.0+                     | VT-x/AMD-V enabled       |

---

## 3. ⚙️ Dependencies

Before using CLMT, ensure your system has:

- [VirtualBox](https://www.virtualbox.org/) 6.x or 7.x
- `VBoxManage` available in your system `PATH`
- [Python](https://www.python.org/) 3.12 or newer

### 🛠️ Troubleshooting
- `VBoxManage` not found? Add VirtualBox to your system `PATH`.
- Python version mismatch? Use `python3` explicitly or update via `pyenv`.

---

## 4. 📥 Installation Guide

### Clone the Repository
```bash
git clone https://github.com/nickolay3132/cyberlab.git
cd cyberlab
```

### Create & Activate a Virtual Environment

🐧 Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

🪟 Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 5. 🚀 Usage

### 🧑‍💻 CLI Commands

All CLI commands are invoked via `clmt.py cli`:

```bash
python clmt.py cli [COMMAND] [OPTIONS]
```

---

**Install Virtual Machines**
```bash
python clmt.py cli install [--skip-download] [--no-verify]
```

| Option           | Description                                                             | Required |
|------------------|-------------------------------------------------------------------------|----------|
| `--skip-download`| Skips downloading OVA files (assumes they are already present locally)  | No       |
| `--no-verify`    | Skips hash verification (faster but less secure)                        | No       |

---

**Start CyberLab**
```bash
python clmt.py cli startup
```

---

**Stop CyberLab**
```bash
python clmt.py cli shutdown [--force]
```

| Option     | Description                                                           | Required |
|------------|-----------------------------------------------------------------------|----------|
| `--force`  | Force immediate shutdown of all VMs (equivalent to pulling the power) | No       |

---

### 📸 Snapshot Management

**Create Snapshot**
```bash
python clmt.py cli snapshot create -n NAME [-d DESCRIPTION]
```

| Option           | Description                                   | Required |
|------------------|-----------------------------------------------|----------|
| `-n`, `--name`   | Snapshot name                                 | Yes      |
| `-d`, `--description` | Optional description (e.g., "Pre-update")| No       |

---

**List Snapshots**
```bash
python clmt.py cli snapshot list
```

---

**Restore Snapshot**
```bash
python clmt.py cli snapshot restore -n NAME
```

| Option           | Description                     | Required |
|------------------|---------------------------------|----------|
| `-n`, `--name`   | Name of the snapshot to restore | Yes      |

---

### 🖼️ GUI Interface

To launch the graphical interface:
```bash
python clmt.py
```

The GUI wraps around the CLI and provides visual access to all features.

---

## 6. ⚙️ Configuration

CLMT no longer uses the current working directory (`cwd`) to locate the configuration file.

Instead:
- The config file (`config.yaml`) must be located next to `clmt.py` or the binary.
- Relative paths defined inside the config are still resolved based on the current working directory.

Example `config.yaml`:
```yaml
storage:
  ova_store_to: ./ova/
  vms_store_to: ./vms/
  import_log_store_to: ./import_log/
```

---

## 7. 📦 Packaging

To build a standalone executable:

```bash
pip install pyinstaller
python build.py
```

### 📂 Output Files

| Platform      | Executable |
|---------------|------------|
| Windows       | `clmt.exe` |
| Linux/macOS   | `clmt`     |

Both files will appear in `./dist/`. The GUI requires the CLI to be present in the same directory.

---

## 8. 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

### Key Permissions
✅ Free to use, modify, and distribute  
✅ Permitted for commercial use  
❌ No liability or warranty

You must include:
- The original copyright:
  ```
  Copyright (c) 2025 Mikalai Viarbila (github.com/nickolay3132)
  ```
- A copy of the license text