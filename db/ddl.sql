-- db/ddl.sql
CREATE DATABASE IF NOT EXISTS pv_school
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS 'pv_user'@'127.0.0.1'
IDENTIFIED BY 'student';

GRANT ALL PRIVILEGES ON pv_school.* TO 'pv_user'@'127.0.0.1';
FLUSH PRIVILEGES;

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

CREATE TABLE IF NOT EXISTS subject (
  id_subject BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(80) NOT NULL,
  code VARCHAR(20) NOT NULL,
  subject_type ENUM('core','elective') NOT NULL DEFAULT 'core',
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_subject),
  UNIQUE KEY uq_subject_code (code)
) ENGINE=InnoDB;

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

CREATE TABLE IF NOT EXISTS class (
  id_class BIGINT NOT NULL AUTO_INCREMENT,
  name VARCHAR(40) NOT NULL,
  school_year SMALLINT NOT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_class),
  UNIQUE KEY uq_class_name_year (name, school_year)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS student (
  id_student BIGINT NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  birth_date DATE NULL,
  class_id BIGINT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_student),
  KEY idx_student_class_id (class_id),
  CONSTRAINT fk_student_class
    FOREIGN KEY (class_id) REFERENCES class(id_class)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

ALTER TABLE student
  ADD COLUMN last_grade_at DATETIME NULL;

CREATE TABLE IF NOT EXISTS grade (
  id_grade BIGINT NOT NULL AUTO_INCREMENT,
  student_id BIGINT NOT NULL,
  subject_id BIGINT NOT NULL,
  teacher_id BIGINT NULL,
  value FLOAT NOT NULL,
  graded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  note VARCHAR(255) NULL,
  PRIMARY KEY (id_grade),
  KEY idx_grade_student (student_id),
  KEY idx_grade_subject (subject_id),
  KEY idx_grade_teacher (teacher_id),
  CONSTRAINT fk_grade_student
    FOREIGN KEY (student_id) REFERENCES student(id_student)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_grade_subject
    FOREIGN KEY (subject_id) REFERENCES subject(id_subject)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_grade_teacher
    FOREIGN KEY (teacher_id) REFERENCES teacher(id_teacher)
    ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS timetable_lesson (
  id_timetable_lesson BIGINT NOT NULL AUTO_INCREMENT,
  class_id BIGINT NOT NULL,
  teacher_id BIGINT NOT NULL,
  subject_id BIGINT NOT NULL,
  weekday TINYINT NOT NULL,
  lesson_no TINYINT NOT NULL,
  room VARCHAR(20) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id_timetable_lesson),
  UNIQUE KEY uq_class_slot (class_id, weekday, lesson_no),
  UNIQUE KEY uq_teacher_slot (teacher_id, weekday, lesson_no),
  CONSTRAINT fk_tt_class
    FOREIGN KEY (class_id) REFERENCES class(id_class)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_tt_teacher
    FOREIGN KEY (teacher_id) REFERENCES teacher(id_teacher)
    ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_tt_subject
    FOREIGN KEY (subject_id) REFERENCES subject(id_subject)
    ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;

CREATE OR REPLACE VIEW v_class_timetable AS
SELECT
  c.id_class AS class_id,
  c.name AS class_name,
  tl.weekday AS weekday,
  tl.lesson_no AS lesson_no,
  s.id_subject AS subject_id,
  s.name AS subject_name,
  t.id_teacher AS teacher_id,
  CONCAT(t.first_name, ' ', t.last_name) AS teacher_name,
  tl.room AS room
FROM timetable_lesson tl
JOIN class c ON c.id_class = tl.class_id
JOIN subject s ON s.id_subject = tl.subject_id
JOIN teacher t ON t.id_teacher = tl.teacher_id;

CREATE OR REPLACE VIEW v_report_class_subject_grades AS
SELECT
  c.id_class AS class_id,
  c.name AS class_name,
  s2.id_subject AS subject_id,
  s2.name AS subject_name,
  COUNT(g.id_grade) AS grade_count,
  AVG(g.value) AS avg_grade,
  MAX(g.graded_at) AS last_graded_at
FROM grade g
JOIN student st ON st.id_student = g.student_id
JOIN class c ON c.id_class = st.class_id
JOIN subject s2 ON s2.id_subject = g.subject_id
GROUP BY
  c.id_class, c.name,
  s2.id_subject, s2.name;
