-- Create Table 
CREATE TABLE tbl_users (
    user_id VARCHAR(20) PRIMARY KEY,
    user_name VARCHAR(20),
    password CHAR(32),
    status INTEGER
)

-- Insert a new user
INSERT INTO tbl_users (
    user_id, 
    user_name, 
    password, 
    status
) VALUES (
    LOWER('krone'), 
    'Krone Cai', 
    MD5(LOWER('krone') || LOWER('123')),
    1
);

-- check login
SELECT COUNT(user_id) AS result FROM tbl_users 
WHERE 
    user_id=LOWER('krone') 
    AND password = MD5(user_id || '123');