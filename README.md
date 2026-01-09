# PV School Backend

Backend application for **PV School** built with **FastAPI**.

This repository contains the backend API used for managing PV School data. The project is designed to be easy to run on school computers, while still using modern Python features and best practices.

---

## 🚀 Overview

* **Framework:** FastAPI
* **Language:** Python
* **API type:** REST
* **Target environment:** School / educational setup

The backend uses modern Python syntax and strict project structure, so correct setup is important.

---

## ⚠️ Python Version Requirement (Very Important)

This project uses **modern Python type hints**, for example:

```python
int | None
```

Because of this, the project **requires Python 3.10 or newer**.

### ✅ Recommended version

* **Python 3.13** (fully supported and tested)

### ❌ Common problem on school computers

On many school PCs, the `python` command still points to **Python 3.9**, even if a newer Python is installed.

This leads to errors such as:

```
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

### ✅ Solution

* Use `py -3.13` instead of `python`
* Or work inside a **virtual environment** (`.venv`)

---

## 📁 Project Structure (Critical)

After downloading the project from GitHub:

1. Download the ZIP archive
2. Extract the ZIP file
3. **Open the correct project root folder**

### ✅ Correct project root must contain:

* `app/`
* `requirements.txt`
* `config/`

### ❌ Common mistake

After extraction, the structure may look like this:

```
pv-school-backend-master/
└── pv-school-backend-master/
    ├── app/
    ├── requirements.txt
```

👉 **Always open the inner folder** (the one containing `app/` and `requirements.txt`).

If you open the wrong folder:

* imports will fail
* IDE inspections will be incorrect
* PyCharm will show false errors

---

## 🧪 Recommended Setup (Virtual Environment)

Run the following commands in the **project root directory**:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### If PowerShell script execution is blocked

You can install dependencies directly using:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## ⚙️ Configuration

1. Copy the example configuration file:

```text
config/config.example.yaml → config/config.yaml
```

2. Edit `config.yaml` and fill in:

   * database credentials
   * environment-specific settings

---

## ▶️ Running the Server

### Option A — Inside virtual environment (recommended)

```powershell
python -m uvicorn app.main:app --reload
```

### Option B — If `python` points to Python 3.9

```powershell
py -3.13 -m uvicorn app.main:app --reload
```

### If `uvicorn` is missing for Python 3.13

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m uvicorn app.main:app --reload
```

---

## 🔍 Verify Python Version (Diagnostics)

To check which Python is actually running:

```powershell
python -c "import sys; print(sys.version); print(sys.executable)"
py -0p
```

Make sure the active Python version is:

* **3.10 or newer**
* ideally **3.13**

---

## 🧠 PyCharm Notes (Red Errors but App Works)

Sometimes the application runs correctly, but PyCharm shows red warnings such as:

```
Unresolved reference 'router'
```

These are **IDE-only issues**, not runtime errors.

### How to fix in PyCharm

1. **Settings → Project → Python Interpreter**

   * select `.venv` or Python 3.13

2. Right-click project root → **Mark Directory as → Sources Root**

3. **File → Invalidate Caches / Restart**

After reindexing, the warnings should disappear.

---

## ✅ Summary

* ✅ Python **3.10+ required** (recommended 3.13)
* ✅ Use **`py -3.13`** or a **virtual environment**
* ✅ Always open the **correct project root folder**
* ⚠️ Red errors in PyCharm do **not** always mean runtime errors

If something works on one PC but not on another, the cause is almost always:

* wrong Python version
* wrong project folder opened
* missing or incorrect virtual environment
