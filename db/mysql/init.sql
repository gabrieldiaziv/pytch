-- matches
CREATE DATABASE pytch;

-- User Table
CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(250) NOT NULL,
    access_token VARCHAR(250),
    refresh_token VARCHAR(250)
);

-- OAuth Session Table
CREATE TABLE OAuth_Session (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50) NOT NULL,
    session_token VARCHAR(250) NOT NULL,
    expires_at VARCHAR(250) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Team Table
CREATE TABLE Team (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    league VARCHAR(50)
);

-- Match Table
CREATE TABLE Match (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    public CHAR(3),
    name VARCHAR(50),
    teamid_home INT,
    teamid_away INT,
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (teamid_home) REFERENCES Team(id) ON DELETE SET NULL,
    FOREIGN KEY (teamid_away) REFERENCES Team(id) ON DELETE SET NULL
);

-- Viz Table
CREATE TABLE Viz (
    viz_id INT PRIMARY KEY AUTO_INCREMENT,
    name CHAR(250) NOT NULL,
    desc CHAR(1000)
);

-- Viz-Match Table
CREATE TABLE Viz_Match (
    match_id INT NOT NULL,
    viz_id INT NOT NULL,
    url CHAR(250) NOT NULL,
    PRIMARY KEY (match_id, viz_id),
    FOREIGN KEY (match_id) REFERENCES Match(match_id) ON DELETE CASCADE,
    FOREIGN KEY (viz_id) REFERENCES Viz(viz_id) ON DELETE CASCADE
);