-- QuestionCraft Database Schema
CREATE DATABASE IF NOT EXISTS smartqbank;
USE smartqbank;

CREATE TABLE IF NOT EXISTS questions (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    subject     VARCHAR(100)  NOT NULL,
    topic       VARCHAR(150)  NOT NULL,
    question    TEXT          NOT NULL,
    option_a    VARCHAR(255)  NOT NULL,
    option_b    VARCHAR(255)  NOT NULL,
    option_c    VARCHAR(255)  NOT NULL,
    option_d    VARCHAR(255)  NOT NULL,
    answer      ENUM('A','B','C','D') NOT NULL,
    difficulty  ENUM('easy','medium','hard') NOT NULL DEFAULT 'medium',
    created_at  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
);
