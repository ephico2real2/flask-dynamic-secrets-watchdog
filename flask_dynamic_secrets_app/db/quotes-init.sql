CREATE DATABASE IF NOT EXISTS quotes;
USE quotes;

-- Create the quotes table with a UNIQUE constraint on the 'quote' column
CREATE TABLE IF NOT EXISTS quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    quote TEXT NOT NULL,
    author VARCHAR(255) NOT NULL,
    UNIQUE(quote(255))
);

-- Insert a sample quote, ignoring the insertion if the quote already exists
INSERT IGNORE INTO quotes (quote, author)
VALUES ('Life is 10% what happens to us and 90% how we react to it.', 'Charles R. Swindoll');
