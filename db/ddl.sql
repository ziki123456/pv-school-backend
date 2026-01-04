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
