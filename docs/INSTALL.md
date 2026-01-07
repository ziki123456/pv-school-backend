# PVSchool – Installation Guide

## 1. Project Overview

PVSchool is a portfolio school management application demonstrating the use of a relational database, repository pattern (D1), database transactions, database views, data import/export, and a graphical user interface.

The application is built using Python and FastAPI and uses MySQL as the relational database system. This document describes how to install and run the application on a standard school PC without using an IDE.

---

## 2. System Requirements

- Operating System: Windows 10 / Windows 11 / Linux
- Python: version 3.11 or higher
- MySQL Server: version 8.x
- Git
- Web browser (Chrome, Firefox, Edge)

---

## 3. Project Download

Clone the project repository from GitHub:

git clone <REPOSITORY_URL>

Navigate to the project directory:

cd PVSchool

---

## 4. Python Virtual Environment

Create a virtual environment:

python -m venv venv

Activate the virtual environment:

Windows:
venv\Scripts\activate

Linux / macOS:
source venv/bin/activate

---

## 5. Install Dependencies

Install required Python packages using pip:

pip install -r requirements.txt

---

## 6. Configuration

The application uses a YAML configuration file.

1. Copy the example configuration file:
config/config.example.yaml

2. Rename it to:
config/config.yaml

3. Edit config/config.yaml and configure:
- database host
- database name
- database user
- database password

If the configuration file is missing or invalid, the application will terminate with an error message.

---

## 7. Database Initialization

Database SQL files are located in the db directory:

- db/ddl.sql – database schema definition
- db/seed.sql – initial test data

Detailed database setup instructions are provided in:
docs/DB_SETUP_MYSQL.md

---

## 8. Application Startup

Start the application using the FastAPI development server:

uvicorn app.main:app --reload

After successful startup, the application will be available at:
http://127.0.0.1:8000

---

## 9. Application Access

Graphical User Interface (GUI):
http://127.0.0.1:8000/

Swagger API documentation:
http://127.0.0.1:8000/docs

---

## 10. Verification

To verify correct installation and configuration:

1. Open the GUI in a web browser
2. Open the Swagger API documentation
3. Call the database health check endpoint:
/api/db/ping

If all steps complete successfully, the application is installed correctly and ready for testing.
