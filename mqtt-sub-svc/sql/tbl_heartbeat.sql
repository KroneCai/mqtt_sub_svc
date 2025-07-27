-- Create Table 
CREATE TABLE tbl_heartbeat (
    dt TIMESTAMP PRIMARY KEY,
    device_id VARCHAR(50),
    power_gear INTEGER,
    status VARCHAR(255),
    software_version VARCHAR(255),
    local_dt TIMESTAMP
)
