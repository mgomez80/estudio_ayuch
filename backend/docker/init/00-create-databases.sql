CREATE DATABASE IF NOT EXISTS db_estudio_ayuch
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE DATABASE IF NOT EXISTS db_estudio_ayuch_auth
  CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE USER IF NOT EXISTS 'dev_user'@'%' IDENTIFIED BY 'dev_pass';
GRANT ALL PRIVILEGES ON db_estudio_ayuch.* TO 'dev_user'@'%';
GRANT ALL PRIVILEGES ON db_estudio_ayuch_auth.* TO 'dev_user'@'%';
FLUSH PRIVILEGES;
