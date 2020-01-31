-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS recruitment_psl_db;
CREATE USER IF NOT EXISTS 'recruitment_psl_dev'@'localhost' IDENTIFIED BY 'recruitment_psl_dev_pwd';
GRANT ALL PRIVILEGES ON `recruitment_psl_db`.* TO 'recruitment_psl_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'recruitment_psl_dev'@'localhost';
FLUSH PRIVILEGES;