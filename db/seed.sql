-- db/seed.sql

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE grade;
TRUNCATE TABLE timetable_lesson;
TRUNCATE TABLE teacher_subject;
TRUNCATE TABLE student;
TRUNCATE TABLE class;
TRUNCATE TABLE subject;
TRUNCATE TABLE teacher;

SET FOREIGN_KEY_CHECKS = 1;

-- TEACHERS
INSERT INTO teacher (id_teacher, first_name, last_name, email, hired_date, is_active) VALUES
(1, 'Jan', 'Novák', 'jan.novak@school.cz', '2020-09-01', 1),
(2, 'Petra', 'Dvořáková', 'petra.dvorakova@school.cz', '2019-09-01', 1),
(3, 'Karel', 'Svoboda', 'karel.svoboda@school.cz', '2021-09-01', 1),
(4, 'Lucie', 'Černá', 'lucie.cerna@school.cz', '2018-09-01', 1);

-- SUBJECTS
INSERT INTO subject (id_subject, name, code, subject_type, is_active) VALUES
(1, 'Matematika', 'MAT', 'core', 1),
(2, 'Čeština', 'CZE', 'core', 1),
(3, 'Angličtina', 'ENG', 'core', 1),
(4, 'Informatika', 'INF', 'elective', 1),
(5, 'Dějepis', 'HIS', 'elective', 1);

-- TEACHER_SUBJECT (M:N)
INSERT INTO teacher_subject (id_teacher_subject, teacher_id, subject_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 2, 3),
(4, 3, 4),
(5, 4, 5);

-- CLASSES
INSERT INTO class (id_class, name, school_year, is_active) VALUES
(1, '1A', 2025, 1),
(2, '1B', 2025, 1),
(3, '2A', 2025, 1);

-- STUDENTS
INSERT INTO student (id_student, first_name, last_name, birth_date, class_id, is_active) VALUES
(1, 'Petr', 'Svoboda', '2008-03-10', 1, 1),
(2, 'Anna', 'Novotná', '2008-06-22', 1, 1),
(3, 'David', 'Bartoš', '2008-09-05', 1, 1),
(4, 'Tomáš', 'Král', '2008-01-15', 2, 1),
(5, 'Eliška', 'Veselá', '2008-11-02', 2, 1),
(6, 'Marie', 'Procházková', '2008-07-19', 2, 1),
(7, 'Jakub', 'Marek', '2007-04-08', 3, 1),
(8, 'Tereza', 'Kučerová', '2007-12-30', 3, 1);

-- TIMETABLE
INSERT INTO timetable_lesson (id_timetable_lesson, class_id, teacher_id, subject_id, weekday, lesson_no, room) VALUES
(1, 1, 1, 1, 1, 1, '101'),
(2, 1, 2, 2, 1, 2, '102'),
(3, 1, 2, 3, 2, 1, '102'),
(4, 1, 3, 4, 3, 3, 'ICT'),
(5, 1, 4, 5, 4, 2, '103'),

(6, 2, 1, 1, 1, 1, '201'),
(7, 2, 2, 2, 2, 2, '202'),
(8, 2, 2, 3, 3, 1, '202'),
(9, 2, 3, 4, 4, 4, 'ICT'),
(10, 2, 4, 5, 5, 2, '203'),

(11, 3, 1, 1, 1, 2, '301'),
(12, 3, 2, 2, 2, 1, '302'),
(13, 3, 2, 3, 3, 2, '302'),
(14, 3, 3, 4, 4, 3, 'ICT'),
(15, 3, 4, 5, 5, 1, '303');

-- GRADES
INSERT INTO grade (id_grade, student_id, subject_id, teacher_id, value, graded_at, note) VALUES
(1, 1, 1, 1, 1.0, '2026-01-02 08:00:00', 'MAT test'),
(2, 1, 2, 2, 2.0, '2026-01-03 09:00:00', 'CZE diktát'),
(3, 2, 1, 1, 1.5, '2026-01-03 10:00:00', 'MAT písemka'),
(4, 3, 3, 2, 2.5, '2026-01-04 11:00:00', 'ENG vocab'),
(5, 4, 1, 1, 3.0, '2026-01-04 12:00:00', 'MAT'),
(6, 5, 4, 3, 1.0, '2026-01-04 13:00:00', 'INF projekt'),
(7, 6, 5, 4, 2.0, '2026-01-05 08:30:00', 'HIS test'),
(8, 7, 3, 2, 1.0, '2026-01-05 09:15:00', 'ENG'),
(9, 8, 2, 2, 2.0, '2026-01-05 10:00:00', 'CZE');

UPDATE student s
SET s.last_grade_at = (
  SELECT MAX(g.graded_at) FROM grade g WHERE g.student_id = s.id_student
);
