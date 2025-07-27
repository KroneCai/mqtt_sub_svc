
CREATE TABLE tbl_devices (
    device_id VARCHAR(20) PRIMARY KEY,
    description VARCHAR(1024),
    type VARCHAR(255),
    model VARCHAR(255),
    spec VARCHAR(255),
    store_id VARCHAR(20),
    equip_date TIMESTAMP,
    status VARCHAR(20)
)
