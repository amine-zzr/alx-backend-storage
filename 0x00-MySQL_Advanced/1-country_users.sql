-- Script to create the 'users' table with constraints, including a country enumeration.
-- The table will store user information with a unique email, and the country field has a default value of 'US'.
-- If the table already exists, this script will not fail.

-- Create 'users' table if it doesn't already exist
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,  -- Primary key, auto-incrementing
    email VARCHAR(255) NOT NULL UNIQUE,          -- Unique email, cannot be null
    name VARCHAR(255),                           -- User's name, optional
    country ENUM('US', 'CO', 'TN') NOT NULL DEFAULT 'US'  -- Country enumeration with default 'US'
);
