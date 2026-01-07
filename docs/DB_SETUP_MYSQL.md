# PVSchool – MySQL Database Setup Guide

## 1. Database System

The PVSchool application uses MySQL Server version 8.x as the relational database management system.
No other database systems are supported.

---

## 2. MySQL Server Installation

Ensure that MySQL Server 8.x is installed and running on the system.
The database can be managed using MySQL Workbench or the MySQL command-line client.

---

## 3. Database Creation

Create a new database for the application:

CREATE DATABASE pvschool
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

---

## 4. Database User Creation

Create a dedicated database user for the application:

CREATE USER 'pvschool_user'@'localhost' IDENTIFIED BY 'strong_password';

---

## 5. User Privileges

Grant required privileges to the application user:

GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE
ON pvschool.*
TO 'pvschool_user'@'localhost';

FLUSH PRIVILEGES;

---

## 6. Database Structure Import

The database structure is defined in the following SQL file:

db/ddl.sql

Import the database schema using the MySQL client:

mysql -u pvschool_user -p pvschool < db/ddl.sql

---

## 7. Initial Data Import

Initial test data is provided in the following file:

db/seed.sql

Import the test data:

mysql -u pvschool_user -p pvschool < db/seed.sql

---

## 8. Configuration File Update

Update the application configuration file:

config/config.yaml

Set the following values:
- database host
- database name: pvschool
- database user: pvschool_user
- database password

---

## 9. Verification

Verify that the database was created correctly:

1. Connect to MySQL
2. Select the database:
   USE pvschool;
3. List tables:
   SHOW TABLES;
4. Verify views:
   SHOW FULL TABLES WHERE TABLE_TYPE = 'VIEW';

If tables and views are visible, the database setup is complete.
