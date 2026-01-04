-- db/ddl.sql
-- MySQL 8.4, InnoDB (transakce, FK)

CREATE TABLE IF NOT EXISTS teacher (
  id_teacher BIGINT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(120) NULL,
  hired_date DATE NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_teacher)
) ENGINE=InnoDB;

-- SUBJECT (obsahuje ENUM -> splní požadavek na "výčet")
CREATE TABLE IF NOT EXISTS subject (
  id_subject BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(80) NOT NULL,
  code VARCHAR(20) NOT NULL,
  subject_type ENUM('core','elective') NOT NULL DEFAULT 'core', -- ENUM
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_subject),
  UNIQUE KEY uq_subject_code (code)
) ENGINE=InnoDB;

-- M:N vazba TEACHER <-> SUBJECT
CREATE TABLE IF NOT EXISTS teacher_subject (
  id_teacher_subject BIGINT NOT NULL AUTO_INCREMENT,
  teacher_id BIGINT NOT NULL,
  subject_id BIGINT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_teacher_subject),
  UNIQUE KEY uq_teacher_subject (teacher_id, subject_id),
  CONSTRAINT fk_teacher_subject_teacher
    FOREIGN KEY (teacher_id) REFERENCES teacher(id_teacher)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_teacher_subject_subject
    FOREIGN KEY (subject_id) REFERENCES subject(id_subject)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

-- CLASS
CREATE TABLE IF NOT EXISTS class (
  id_class BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(40) NOT NULL,              -- např. "1A"
  school_year SMALLINT NOT NULL,          -- např. 2025
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_class),
  UNIQUE KEY uq_class_name_year (name, school_year)
) ENGINE=InnoDB;

-- STUDENT (FK na class)
CREATE TABLE IF NOT EXISTS student (
  id_student BIGINT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  birth_date DATE NULL,                   -- datový typ DATE
  class_id BIGINT NULL,                   -- student může být zatím bez třídy
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_student),
  KEY idx_student_class_id (class_id),
  CONSTRAINT fk_student_class
    FOREIGN KEY (class_id) REFERENCES class(id_class)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;
