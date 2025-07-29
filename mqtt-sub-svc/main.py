from loguru import logger
from threading import Thread
from mqtt.mqtt import MQTT
from config import settings

def run():
    mqtt_sub = MQTT()
    mqtt_sub.forever()
    
def main():
    logger.add(settings.LOG_PATH, rotation="10 MB")
    subs = Thread(target = run, daemon=True, name="MQTT_Subscriber")
    subs.start()
    subs.join()


if __name__ == '__main__':
    main()
    