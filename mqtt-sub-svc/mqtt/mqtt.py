from datetime import datetime
# from email import message
from loguru import logger
# import random
import time
import json
# import sys
from config import settings
import paho.mqtt.client as mqtt
from db.db import Database
from sqlalchemy import text
from model.model import MQTTLog, MQTTMessage
from utils.AESCiper import AESCiper
from utils.logger import Logger

broker = settings.MQTT_BROKER
port = settings.MQTT_PORT
qos = settings.MQTT_QOS
client_id = settings.MQTT_CLIENT_ID
user_name = settings.MQTT_USER_NAME
password = settings.MQTT_PASSWORD
topic = settings.MQTT_TOPIC
aes_key = settings.key
aes_iv = settings.iv

class MQTT:
    # 构造函数
    def __init__(self):
        # 创建数据库连接
        self.database = Database()
        self.engine = self.database.get_db_connection()
        self.session = self.database.get_db_session(self.engine)
        self.logger = Logger()

        logger.info(f'Initializing MQTT client[id={client_id}], [broker={broker}:{port}]')
        self.logger.add_log("INFO", f"Initializing MQTT client[id={client_id}], [broker={broker}:{port}]")
        
        # 创建MQTT客户端
        self.client = mqtt.Client(
            client_id=client_id,
            clean_session=False,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            userdata={
                "session": self.session,
                "client_id": client_id,
            },
        )
        self.client.username_pw_set(username=user_name, password=password)
        self.__errorCount = 0
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        while (self.__errorCount < 10):
            try:
                self.client.connect(broker, port)
                break
            except Exception as e:
                self.__errorCount += 1
                logger.error(f'Failed to connect to broker: {e}, trying to reconnect [{self.__errorCount}/10]')
                self.logger.add_log("ERROR", f"Failed to connect to broker: {e}, trying to reconnect [{self.__errorCount}/10]")  

                time.sleep(10) # 暂停10秒
        else:
            logger.error(f'Failed to connect to MQTT broker after 10 attempts.')
            self.logger.add_log("ERROR", f"Failed to connect to MQTT broker after 10 attempts.")
    
    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info(f'MQTT broker connected.')
            self.logger.add_log("INFO", f"MQTT broker connected.")
            result = client.subscribe(topic=topic, qos=qos)
            if result[0] == 0:
                logger.info(f"Subscribed to topic: {topic}")
                self.logger.add_log("INFO", f"Subscribed to topic: {topic}")
            else:
                logger.error(f"Failed to subscribe to topic: {topic}, error code: {result[0]}")
                self.logger.add_log("ERROR", f"Failed to subscribe to topic: {topic}, error code: {result[0]}")
        else:
            logger.error(f"Failed to connect to MQTT broker, reason code: {reason_code}")
            self.logger.add_log("ERROR", f"Failed to connect to MQTT broker, reason code: {reason_code}")

    def on_disconnect(self, client, userdata, flags, reason_code, properties):
        logger.info(f"Disconnected from MQTT broker, reason code: {reason_code}")
        self.logger.add_log("INFO", f"Disconnected from MQTT broker, reason code: {reason_code}")
    
    def on_message(self, client, userdata, msg):
        '''Step 1: 获取topic信息'''
        topic = str(msg.topic).strip()

        '''Step 2: 解析topic
        终端上传数据的主题分为4级  /厂家标识/产品类别/设备硬件型号/IMEI
        比如 /nengduojie/mousetrap/nb-001/869373063900360
        厂家标识： nengduojie;
        产品类别:  mousetrap-捕鼠器；
        设备类别： node: 终端  gw- lora: 网关  nb: NB终端  001:该类别的硬件版本型;
        设备ID: 869373063900360
        '''
        topic_factory = ""
        topic_product = ""
        topic_device_type = ""
        topic_device_id = ""
        try:
            info = topic.split('/')
            if info[0] == "":
                info = info[1:]
            topic_factory = info[0]
            topic_product = info[1]
            topic_device_type = info[2]
            topic_device_id = info[3]
        except Exception as e:
            logger.error(f'Failed to parse topic: {e}')
            self.logger.add_log("ERROR", f"Failed to parse topic: {e}")
            return
        # print(topic_factory, topic_product, topic_device_type, topic_device_id)

        '''Step 3: 对接收到的payload进行解密
        根据厂家设计,所有的数据都进行了AES-128数据加密,加密类型为CBC,采用Zero Padding填充。
        密钥和偏移量为: key= 'AQRTYUOIFSRBFCEG', iv= 'AQRTYUOIFSRBFCEG'。
        '''
        payload = ""
        try:
            ciper = AESCiper(aes_key, aes_iv)
            payload = ciper.decrypt(msg.payload)
        except Exception as e:
            logger.error(f'Failed to decrypt payload: {e}')
            self.logger.add_log("ERROR", f"Failed to decrypt payload: {e}")
            return
        
        '''Step 4: 解析payload
        解密后的payload为JSON格式。以下为测试用数据。
        payload = {"type":"nb_maintain","timestamp":1753453058,"CCID":"898604B60322D0300881","T":24,"com":"NB-IOT","csq":"17","crc":"ABCD1234","version":"2.0.2","bat":3516,"model":"002"}
        payload = {"type":"triggle_cnt","cnt_L":10,"cnt_R":0,"timestamp":1697964022,"bat":3566,"T":26,"csq":"20"}
        payload = {"type":"first_triggle","side":1,"triggle_time":1753453058,"timestamp":1697964022,"bat":3566,"T":26,"csq":"20"}
        paylaod = {"type":"sensor_state","T_state":1,"time":"1697964022","timestamp":1697964022,"bat":3566,"T":26,"csq":"20"}
        '''
        try:
            payload = json.loads(payload)
            msg_type = payload["type"] # 消息类型：nb_maintain, first_triggle, triggle_cnt, sensor_state
            msg_ts = payload["timestamp"] # 时间戳
            msg_temp = payload["T"] # 温度
            msg_csq = payload["csq"] # 信号强度
            msg_bat = payload["bat"] # 电池电量
            msg_ccid = "" # 卡识别码
            msg_com = "" # 通信方式，例如”NB-IOT“
            msg_crc = "" # 校验码
            msg_version = "" # 固件版本号
            msg_side = 0 # 触发侧：1-左侧触发；2-右侧触发
            msg_triggle_time = msg_ts # 首次触发时间
            msg_cnt_L = 0 # 左侧触发次数
            msg_cnt_R = 0 # 右侧触发次数
            msg_T_state = 0 # 高温报警及温度恢复故障类型 1-高温报警；0-温度恢复
            msg_time = "" # 时间
            match msg_type:
                case "nb_maintain": # 维保操作
                    msg_ccid = payload["CCID"]
                    msg_com = payload["com"]
                    msg_crc = payload["crc"]
                    msg_version = payload["version"]
                case "first_triggle": # 首次触发
                    msg_side = payload["side"]
                    msg_triggle_time = payload["triggle_time"]
                case "triggle_cnt": # 触发次数日统计
                    msg_cnt_L = payload["cnt_L"] 
                    msg_cnt_R = payload["cnt_R"]
                case "sensor_state": # 高温报警及温度恢复
                    msg_T_state = payload["T_state"]
                    msg_time = payload["time"]
                case _:
                    logger.error(f'Unknown message type: {msg_type}')
                    self.logger.add_log("ERROR", f"Unknown message type: {msg_type}")
                    return
            
            msg = MQTTMessage(
                ts = datetime.now(),
                topic = topic,
                t_factory = topic_factory,
                t_product = topic_product,
                t_device_type = topic_device_type,
                t_device_id = topic_device_id,
                qos = msg.qos,
                payload_encrypted = msg.payload,
                payload_decrypted = payload,
                client_id = client_id,
                msg_type = msg_type,
                msg_ts = datetime.fromtimestamp(msg_ts),
                msg_temp = msg_temp,
                msg_csq = msg_csq,
                msg_bat = msg_bat,
                msg_ccid = msg_ccid,
                msg_com = msg_com,
                msg_crc = msg_crc,
                msg_version = msg_version,
                msg_side = msg_side,
                msg_triggle_time = datetime.fromtimestamp(msg_triggle_time),
                msg_cnt_L = msg_cnt_L,
                msg_cnt_R = msg_cnt_R,
                msg_T_state = msg_T_state,
                msg_time = msg_time,)
            count = self.session.execute(text("SELECT count(1) as count FROM tbl_mqtt_message where t_device_id = :device_id and msg_type = :msg_type and msg_ts > :msg_ts - interval '30 seconds'"), {"device_id": topic_device_id, "msg_type": msg_type, "msg_ts": datetime.fromtimestamp(msg_ts)}).scalar()
            if count == 0:
                self.session.add(msg) # 添加数据
                self.session.commit() # 提交事务，保存到数据库
                logger.info(f"Message from {topic} is saved.")
                self.logger.add_log("INFO", f"Message from {topic} is saved.")
            else:
                logger.info(f"Message from {topic} is duplicated, not saved.")
                self.logger.add_log("INFO", f"Message from {topic} is duplicated, not saved.")
        except Exception as e:
            logger.error(f'Failed to parse and save payload: {e}')
            self.logger.add_log("ERROR", f"Failed to parse and save payload: {e}")
            return
        
    # 启动网络循环
    def forever(self):
        self.client.loop_forever()