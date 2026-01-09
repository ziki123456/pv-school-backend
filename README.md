# PV School Backend

Backend application for PV School built with **FastAPI**.

This repository contains the backend API used for managing PV School data. The project is intended primarily for a school environment and focuses on clarity, reproducibility, and correct setup across different computers.

---

## Overview

* **Framework:** FastAPI
* **Language:** Python
* **API type:** REST
* **Environment:** Educational / school setup

The backend uses modern Python features and a strict project structure. Correct configuration is therefore essential.

---

## Python Version Requirement

This project uses modern Python type hints, for example:

```python
int | None
```

Because of this, **Python 3.10 or newer is required**.

### Recommended version

* Python 3.13

### Common issue on school computers

On many school computers, the `python` command still points to Python 3.9, even if a newer Python version is installed.

This causes runtime errors such as:

```
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

### Solution

* Use `py -3.13` instead of `python`, or
* Work inside a virtual environment (`.venv`)

---

## Project Structure

After downloading the project from GitHub:

1. Download the ZIP archive
2. Extract the ZIP
3. Open the correct project root directory

### Correct project root contains

* `app/`
* `requirements.txt`
* `config/`

### Common mistake

After extraction, the directory structure may look like this:

```
pv-school-backend-master/
└── pv-school-backend-master/
    ├── app/
    ├── requirements.txt
```

Always open the inner directory (the one containing `app/` and `requirements.txt`).

Opening the wrong directory leads to:

* broken imports
* incorrect IDE inspections
* misleading errors in PyCharm

---

## Virtual Environment Setup (Recommended)

Run the following commands in the project root directory:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

### If PowerShell script execution is blocked

Install dependencies directly using:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## Configuration

1. Copy the example configuration file:

```
config/config.example.yaml → config/config.yaml
```

2. Edit `config.yaml` and fill in the required values:

* database credentials
* environment-specific settings

---

## Running the Server

### Option A — Using the virtual environment

```powershell
python -m uvicorn app.main:app --reload
```

### Option B — If `python` points to an older version

```powershell
py -3.13 -m uvicorn app.main:app --reload
```

### If `uvicorn` is not installed for Python 3.13

```powershell
py -3.13 -m pip install -r requirements.txt
py -3.13 -m uvicorn app.main:app --reload
```

---

## Python Version Diagnostics

To verify which Python interpreter is being used:

```powershell
python -c "import sys; print(sys.version); print(sys.executable)"
py -0p
```

Ensure the active Python version is 3.10 or newer (ideally 3.13).

---

## PyCharm Notes

In some cases, the application runs correctly, but PyCharm displays warnings such as:

```
Unresolved reference 'router'
```

These warnings are IDE-related and do not indicate runtime errors.

### How to fix in PyCharm

1. Open **Settings → Project → Python Interpreter** and select `.venv` or Python 3.13
2. Right-click the project root and select **Mark Directory as → Sources Root**
3. Go to **File → Invalidate Caches / Restart**

After reindexing, the warnings should disappear.

---

## Summary

* Python 3.10 or newer is required
* Python 3.13 is recommended
* Always open the correct project root directory
* Prefer using a virtual environment
* IDE warnings do not necessarily indicate runtime errors

If the project behaves differently across computers, the most common causes are:

* incorrect Python version
* wrong project directory opened
* missing or misconfigured virtual environment
