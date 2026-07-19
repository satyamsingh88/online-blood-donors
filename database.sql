CREATE DATABASE blood_donor_db;
USE blood_donor_db;

-- Table for registered donors
CREATE TABLE donors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    gender VARCHAR(10),
    blood_group VARCHAR(5) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    address TEXT NOT NULL,
    reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table for blood requests
CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_name VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    location VARCHAR(100) NOT NULL,
    contact VARCHAR(15) NOT NULL,
    needed_date DATE NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending'
);

-- Table for Admin Users
CREATE TABLE  users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Default Admin (User: admin, Pass: admin123)
INSERT INTO users (username, password) VALUES ('admin', 'admin123');