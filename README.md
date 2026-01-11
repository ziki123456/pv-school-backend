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

1. Copy the example configuration file (This project does NOT include `config.yaml` in the repository so you have to create it)
:

```
config/config.example.yaml → config/config.yaml
```

2. Edit `config.yaml` and fill in the required values:

* database credentials
* environment-specific settings

---
## Database Initialization (MySQL)

The project includes an SQL script that automatically creates:

- the database `pv_school`
- a database user `pv_user`
- required privileges for the application

No manual database or user creation is needed, as long as the script is executed correctly.

### What the script does

The following operations are performed:

- creates the database `pv_school` (if it does not already exist)
- creates the MySQL user `pv_user` (if it does not already exist)
- grants full access to the `pv_school` database
- applies UTF-8 encoding (`utf8mb4`)

### How to run the script in MySQL Workbench

1. Open **MySQL Workbench**
2. Connect to your local MySQL server  
   (usually as `root` or another administrative user)
3. Open a new SQL tab
4. Paste the provided SQL script into the editor
5. Click **Execute** (lightning bolt icon)

If the script runs without errors, the database and user are ready to use.

### Application connection

After running the script, configure the application to use:

- **Database:** `pv_school`
- **User:** `pv_user`
- **Password:** `student`
- **Host:** `127.0.0.1`

Once the connection details are set correctly in the configuration file, the backend can connect to the database without any additional setup.


## Running the Application from Command Line (Required)

This project **must be runnable without any IDE**.  
The following steps describe how to run the application **only using Command Prompt or PowerShell** on any computer.

---

### 1. Open Command Line in the project root

After downloading and extracting the project from GitHub:

1. Open **File Explorer**
2. Navigate to the folder that contains:
   - `app/`
   - `requirements.txt`
   - `config/`
3. Click into the address bar
4. Type `cmd` and press **Enter**

This opens **Command Prompt directly in the correct project directory**.

---

### 2. Verify available Python versions

Run:

```powershell
py -0p
```

Ensure that **Python 3.10 or newer** is available  
(Recommended version: **Python 3.13**).

---

### 3. Create a virtual environment

In the project root directory, run:

```powershell
py -3.13 -m venv .venv
```

If Python 3.13 is not available, use any version **≥ 3.10**, for example:

```powershell
py -3.11 -m venv .venv
```

---

### 4. Activate the virtual environment

**PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Command Prompt (CMD):**
```cmd
.venv\Scripts\activate.bat
```

After activation, the command line should start with:

```
(.venv)
```

---

### 5. Install project dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If this fails, use the explicit interpreter:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

### 6. Create and configure the configuration file

This repository does **not** include `config.yaml`.

1. Copy:
```
config/config.example.yaml
```

2. Rename it to:
```
config/config.yaml
```

3. Edit `config.yaml` and set correct database connection values.

---

### 7. Initialize the MySQL database

Run the provided SQL script in **MySQL Workbench**.

The script automatically:
- creates database `pv_school`
- creates user `pv_user`
- grants required privileges

After successful execution, the database is ready.

---

### 8. Start the FastAPI server

Run:

```powershell
python -m uvicorn app.main:app --reload
```

If `python` points to an older version:

```powershell
py -3.13 -m uvicorn app.main:app --reload
```

---

### 9. Verify the application is running

Open a web browser:

- GUI:  
  http://127.0.0.1:8000/

- API documentation (Swagger):  
  http://127.0.0.1:8000/docs

If these pages load correctly, the application is running.

---

## Notes for Evaluation

- The application **does not require PyCharm or any IDE**
- All steps can be executed using **Command Prompt / PowerShell only**
- Using a virtual environment is required
- Python version must be **3.10 or newer**

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
