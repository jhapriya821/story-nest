CREATE DATABASE story_nest_db;
USE story_nest_db;
CREATE TABLE stories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_name VARCHAR(100),
    theme VARCHAR(100),
    story_text TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
SELECT * FROM stories;