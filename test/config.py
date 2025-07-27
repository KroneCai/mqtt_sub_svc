# Database Setttings
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://kronecai@localhost:5432/mqtt_db"

# MQTT Settings
MQTT_BROKER = "47.111.93.153"
MQTT_PORT = 1883
MQTT_QOS = 1 # 0-最多一次, 1-至少一次, 2-恰好一次
MQTT_TOPIC_SUB = "/nengduojie/#"
MQTT_CLIENT_ID = "server_test01"
MQTT_USERNAME = "riot_pub_dev"
MQTT_PASSWORD = "rent@kil2025"

# Encryption & Decryption Settings
ENCRYPTION_ALGORITHM = "AES-128"
ENCRYPTION_KEY = "AQRTYUOIFSRBFCEG"  # 16字节的密钥
ENCRYPTION_IV = "AQRTYUOIFSRBFCEG"  # 16字节的IV
