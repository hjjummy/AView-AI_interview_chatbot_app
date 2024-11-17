CREATE TABLE users (
    IdUser INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    gender ENUM('male', 'female') NOT NULL,
    age INT NOT NULL,
    role ENUM('interviewer', 'interviewee') NOT NULL
);
