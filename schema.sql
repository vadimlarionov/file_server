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
CREATE TABLE IF NOT EXISTS Groups(
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(256) NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  is_deleted TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

CREATE TABLE IF NOT EXISTS UserGroup(
  user_id INT NOT NULL,
  group_id INT NOT NULL,
  PRIMARY KEY (user_id, group_id),
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (group_id) REFERENCES Groups(id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

CREATE TABLE IF NOT EXISTS Catalogue(
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(256) NOT NULL,
  author_id INT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (author_id) REFERENCES User(id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

CREATE TABLE IF NOT EXISTS File(
  id INT NOT NULL AUTO_INCREMENT,
  path VARCHAR(256) NOT NULL,
  title VARCHAR(256) NOT NULL,
  description VARCHAR(1024) NULL,
  attributes VARCHAR(256) NULL,
  other_attributes VARCHAR(256) NULL,
  user_id INT NOT NULL,
  catalogue_id INT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES User(id),
  FOREIGN KEY (catalogue_id) REFERENCES Catalogue(id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

CREATE TABLE IF NOT EXISTS GroupsCatalogue(
  group_id INT NOT NULL,
  catalogue_id INT NOT NULL,
  permission INT,   -- 1-read, 2-write, 3-read and write
  PRIMARY KEY (group_id, catalogue_id),
  FOREIGN KEY (group_id) REFERENCES Groups(id),
  FOREIGN KEY (catalogue_id) REFERENCES Catalogue(id)
) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

# -- Пользователи, добавленные к каталогу
# CREATE TABLE IF NOT EXISTS UserCatalogue(
#   catalogue_id INT NOT NULL,
#   userd_id INT NOT NULL,
#   FOREIGN KEY (user_id) REFERENCES User(id),
#   FOREIGN KEY (catalogue_id) REFERENCES Catalogue(id)
# ) ENGINE = InnoDB DEFAULT CHARACTER SET = 'utf8';

-- ----- CREATE USER ----- --
GRANT USAGE ON *.* TO 'fs_user'@'localhost'; -- Официальный хак для DROP IF EXISTS
DROP USER 'fs_user'@'localhost';
CREATE USER 'fs_user'@'localhost' IDENTIFIED BY '8kf5XvcLCqNQ';
GRANT INSERT, SELECT, UPDATE, DELETE ON fs_db . * TO 'fs_user'@'localhost';

-- ----- DEBUG ----- --
INSERT INTO fs_db.User(id, username, password, is_admin) VALUES (1, 'root', 'root', TRUE);
INSERT INTO fs_db.User(id, username, password, is_admin) VALUES (2, 'vadim', 'vadim', TRUE);
INSERT INTO fs_db.Groups(id, title) VALUES (1, 'IU5-18');
INSERT INTO fs_db.Groups(id, title) VALUES (2, 'IU5-17');
INSERT INTO fs_db.Groups(id, title) VALUES (3, 'Professor');

INSERT INTO fs_db.UserGroup(user_id, group_id) VALUES (1, 3);
INSERT INTO fs_db.UserGroup(user_id, group_id) VALUES (2, 1);
