# PVSchool – Project Checklist

This checklist demonstrates compliance with the assignment requirements.
Each requirement is marked as completed and references where it can be verified.

---

## General Requirements

- [x] **Relational database used**
  - MySQL Server 8.x
  - Verified in: db/ddl.sql

- [x] **Repository pattern implemented (D1)**
  - Custom repositories without ORM
  - Verified in: app/db/repositories/

- [x] **Application configuration via configuration file**
  - YAML configuration file
  - Verified in: config/config.yaml

---

## Database Requirements

- [x] **Minimum of 5 tables**
  - teacher
  - student
  - class
  - subject
  - grade
  - timetable_lesson
  - teacher_subject
  - Verified in: db/ddl.sql

- [x] **Many-to-many relationship**
  - teacher ↔ subject
  - Verified in: teacher_subject table

- [x] **Minimum of 2 database views**
  - v_class_timetable
  - v_report_class_subject_grades
  - Verified in: db/ddl.sql

- [x] **Required data types**
  - String (VARCHAR): names, emails
  - Enum: subject_type
  - Float: grade value
  - Date / DateTime: last_grade_at, timetable data
  - Boolean equivalent: TINYINT(1)
  - Verified in: db/ddl.sql

---

## Application Functionality

- [x] **CRUD operations implemented**
  - Create and read operations for core entities
  - Verified via API and GUI

- [x] **Multi-table operation**
  - Grade insertion affects grade and student tables
  - Verified in: GradeRepository

- [x] **Transaction over multiple tables**
  - Insert grade + update student timestamp
  - Verified in: GradeRepository transaction logic

- [x] **Aggregated report from at least 3 tables**
  - Class-subject-grade report
  - Verified via database view and API endpoint

---

## Import / Export

- [x] **Data import into at least 2 tables**
  - Teachers import
  - Students import
  - CSV format
  - Verified in: ImportRepository

- [x] **Data export**
  - Teachers export
  - Students export
  - CSV format
  - Verified in: ExportRepository

---

## User Interface

- [x] **Graphical user interface provided**
  - Dashboard
  - Timetable view
  - Report view
  - Verified in: app/gui/templates/

---

## Error Handling

- [x] **Input validation**
  - Invalid IDs and missing data handled
  - Verified via API responses

- [x] **Database connection error handling**
  - Application fails gracefully on connection error
  - Verified in: database connection logic

- [x] **Configuration error handling**
  - Missing or invalid configuration detected on startup
  - Verified in: application startup

---

## Testing and Documentation

- [x] **Installation documentation provided**
  - docs/INSTALL.md

- [x] **Database setup documentation provided**
  - docs/DB_SETUP_MYSQL.md

- [x] **Test setup scenario provided**
  - docs/TEST_SETUP.pdf

- [x] **Functional test scenarios provided**
  - docs/TEST_SCENARIO_FUNCTIONAL.pdf

- [x] **Error test scenarios provided**
  - docs/TEST_SCENARIO_ERRORS.pdf

---

## Final Status

All mandatory assignment requirements have been implemented and documented.
