DROP DATABASE IF EXISTS fs_db;

CREATE DATABASE fs_db
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

USE fs_db;

-- ----- CREATE TABLES ----- --
CREATE TABLE IF NOT EXISTS User(
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(70) NOT NULL,
  password VARCHAR(50) NOT NULL,
  is_admin TINYINT(1) NOT NULL DEFAULT 0,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id),
  UNIQUE KEY (username)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

CREATE TABLE IF NOT EXISTS Session(
  session_key VARCHAR(40),
  user_id INT,
  expire_date DATETIME,
  PRIMARY KEY (session_key),
  INDEX (user_id),
  FOREIGN KEY (user_id) REFERENCES User(id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

-- Ключевое слово Group зарезервировано. Поэтому используем Groups
-- У группы должен быть author_id, но его убираем для упрощения. Всё создаёт админ
CREATE TABLE IF NOT EXISTS Groups(
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(256) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

CREATE TABLE IF NOT EXISTS User_group(
  user_id INT NOT NULL,
  group_id INT NOT NULL,
  permission TINYINT UNSIGNED NOT NULL, -- Будут похожи на права в linux
  PRIMARY KEY (user_id, group_id),
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (group_id) REFERENCES Groups(id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

-- ----- CREATE USER ----- --
DROP USER 'fs_user'@'localhost';
CREATE USER 'fs_user'@'localhost' IDENTIFIED BY '8kf5XvcLCqNQ';
GRANT INSERT, SELECT, UPDATE ON fs_db . * TO 'fs_user'@'localhost';

INSERT INTO fs_db.User(id, username, password, is_admin) VALUES (1, 'root', 'root', TRUE);
INSERT INTO fs_db.Groups(id, title) VALUES (1, 'Home assignment');
INSERT INTO fs_db.User_group(user_id, group_id, permission) VALUES (1, 1, 7);
