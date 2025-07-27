-- Create Table 
CREATE TABLE tbl_mqtt_log (
    dt TIMESTAMP PRIMARY KEY DEFAULT(NOW()),
    host VARCHAR(50),
    port INTEGER,
    topic VARCHAR(255),
    user_data VARCHAR(255),
    message VARCHAR(65535)
)
