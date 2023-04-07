
CREATE DATABASE IF NOT EXISTS dateplanner;
USE dateplanner;

DROP TABLE IF EXISTS Users CASCADE;
DROP TABLE IF EXISTS SearchData CASCADE;

CREATE TABLE Users(
    user_id int4 AUTO_INCREMENT,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(255),
    dob DATE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE SearchData(
    location VARCHAR(255),
    date DATE,
    budget INT,
    preference VARCHAR(255),
    weather VARCHAR(255),
    PAIMARY KEY(user_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)