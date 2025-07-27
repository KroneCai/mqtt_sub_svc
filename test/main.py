import paho.mqtt.client as mqtt
import config
import time
from AESCiper import AESCiper
from sqlalchemy import create_engine,text

def main():
    # Test db connection
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    try:
        with engine.connect() as conn:
            # 执行简单查询验证连接
            result = conn.execute(text("SELECT 1"))
            if result.scalar() == 1:
                print("✅ 数据库连接测试成功")
    except OperationalError as e:
        print(f"🚨 连接失败 - 网络/服务问题: {e}")
    except SQLAlchemyError as e:
        print(f"🚨 连接失败 - 数据库错误: {e}")

    # Test AES encryption and decryption
    key = config.ENCRYPTION_KEY
    iv = config.ENCRYPTION_IV
    ciper = AESCiper(key, iv)
    data = "Hello World!"
    encrypted_data = ciper.encrypt(data)
    print(encrypted_data)
    a1 = b'\xd1\x01\xee\x93\x06\x1f\xda\x9cg9\xda\nI\xd1\xa1\xc5\x04\x12\xd7\xa1r\xc5\x7f\x95\xd9\x88.\xfb\x9b\xd8\xa4\xcdRB]\xa9P\xe3:\x96\xa3\xf1\x11^\xe5g@\xe9\x95\x91\xc7\xfc(\x85\xff\xde,\xa3\x93\xb5\xbd\x805\xab\x90\xc0\xc6\xd4\xf0\x88\xaba\xbd\x8a\xa5l[z\xc3:x\xc1:\x05\xd1N\xfc\xed\xf6\xd7\x1c\xdc\xd3Z\xb0\xef\x03\xaf\xee/\x80\x0fabv\x18=\xd9\xde\xa5\xa6ct,\x94FHg\xd8\x12\xae\xee\xcb\x98\x16R\x0fe\x14\xf9\xa8\x11n5 \xc1\xb8a\xb5\xda\x0c\xbd\xbap\xb2\xbc\xdb.\xcb0\x1c\xf6=\xa2\x87<\xf6[p`\xa5&\x99 qd\x15g\x1ao\xe0\x86\x18c"\x0c'
    a2 = b"\xd1\x01\xee\x93\x06\x1f\xda\x9cg9\xda\nI\xd1\xa1\xc5\x04\x12\xd7\xa1r\xc5\x7f\x95\xd9\x88.\xfb\x9b\xd8\xa4\xcdj\x9bX\xbb\xdb\xbaY\x86\xc1\xe3\xb2G\x9cD<C\x9eN\xd5\xa9\xc8\x94iE\xdc\x81\x92\xf7\xb7S\x04\xc4\xa7\xcb\x94\xa0\x0f{X\xdf4(9\xc0~\x93\xe7\xab\xed\x9f@\x9cgj\xc7}\x02\x97wUUv\xb7*\xc7\x86\x97\x82 XJ&\x83\xd1\x04G\xffP\xdc\xb6\xbc\xa8\xb3}I\xf6\xac\x13\xf5=\xb7>\x86\xed\x04\xe1\xa0\x08'=\xe3\xee\x88\xb8\xbc\xa8/\xe5CH|\xf8\x97'\x13^\xfc\x95\xb0\x81#\x93\x18\x85\x04\xe3\xd6l\x1ee\x99<\xa6\xb2\x1f\xb3\x04\xea\xd0i\x05\xc7\xfc\xbc"
    a3 = b"\xd1\x01\xee\x93\x06\x1f\xda\x9cg9\xda\nI\xd1\xa1\xc5\x04\x12\xd7\xa1r\xc5\x7f\x95\xd9\x88.\xfb\x9b\xd8\xa4\xcd'\xc8\x11K\x1fW4\xd7\x8d\xe6y\xfe/\xb4\x98\x9d\xbf\x15\xc2.\x1e#\x8dZ\x83\xaeo7\xb0\x8f\x8d\x90\x82\x85\xbb]\xfca\x99n\xf2R!c\xea\x9a;\x03\xf1\xfbh\xc2\xf6\x08\x01\x01\x83,xZ\xca\x9b\xc8\xac\xb7M\xfb\x1e\x8b|\x0b$]\xbf+\xd9\x98L>t|\x0b\xd7\xbaY\xe5\x89[V\x84\xe1\xf2\xf6\xf0\xbb2\x0b<DD\xcd\xff\x9c\x08\xc4\x11\xe6K\xb6r$w{\xc2\xf5\xb6\xd2kD\x8e\xb0\x7f\x8b\xd9\xf2\x06d\x9f:\x9c\x93\x84\xed\x9a,\xd9\xe09\t\x8cn\x8dm\xf8"
    decrypted_data = ciper.decrypt(a1)
    print(decrypted_data)
    decrypted_data = ciper.decrypt(a2)
    print(decrypted_data)
    decrypted_data = ciper.decrypt(a3)
    print(decrypted_data)
    decrypted_data = ciper.decrypt(encrypted_data)
    print(decrypted_data)
    

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)  
    client.client_id = config.MQTT_CLIENT_ID
    client.qos = config.MQTT_QOS
    client.topics = config.MQTT_TOPIC_SUB
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    try:
        print("正在连接MQTT broker: ", config.MQTT_BROKER)
        result = client.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
        if result == 0:
            print("MQTT broker连接成功")
        else:
            print(f"MQTT broker连接失败，错误代码: {result}")
            return
    except Exception as e:
        print(f"连接MQTT broker时发生异常: {e}")
        return
    
    print("开始监听MQTT消息...")
    print(f"订阅主题: {config.MQTT_TOPIC_SUB}")
    print("按 Ctrl+C 退出程序")
    
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n正在断开连接...")
        client.disconnect()
        print("程序已退出")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"已连接到MQTT broker，返回码: {reason_code}")
    if reason_code == 0:
        print(f"正在订阅主题: {config.MQTT_TOPIC_SUB}")
        result = client.subscribe(config.MQTT_TOPIC_SUB, config.MQTT_QOS)
        if result[0] == 0:
            print("主题订阅成功")
        else:
            print(f"主题订阅失败，错误代码: {result[0]}")
    else:
        print(f"连接失败，原因码: {reason_code}")

def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"与MQTT broker断开连接，原因码: {reason_code}")

def on_message(client, userdata, msg):
    print(f"收到消息 - 主题: {msg.topic}, 内容: {msg.payload}")

if __name__ == '__main__':
    main()