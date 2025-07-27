#!/usr/bin/env python3
"""
MQTT客户端测试脚本
用于测试MQTT订阅服务是否能正常持续运行
"""

import subprocess
import sys
import os
import time
import signal

def test_mqtt_client():
    """测试MQTT客户端"""
    print("=" * 50)
    print("MQTT客户端测试")
    print("=" * 50)
    
    # 确保在正确的目录
    test_dir = "/Users/kronecai/project/mqtt_sub_svc/test"
    os.chdir(test_dir)
    print(f"当前工作目录: {os.getcwd()}")
    
    # 检查依赖
    print("\n1. 检查依赖包...")
    try:
        import paho.mqtt.client as mqtt
        print("✓ paho-mqtt 已安装")
    except ImportError:
        print("✗ paho-mqtt 未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "paho-mqtt"], check=True)
        print("✓ paho-mqtt 安装完成")
    
    # 检查配置文件
    print("\n2. 检查配置文件...")
    if os.path.exists("config.py"):
        print("✓ config.py 存在")
        import config
        print(f"  MQTT Broker: {config.MQTT_BROKER}:{config.MQTT_PORT}")
        print(f"  订阅主题: {config.MQTT_TOPIC_SUB}")
        print(f"  客户端ID: {config.MQTT_CLIENT_ID}")
    else:
        print("✗ config.py 不存在")
        return False
    
    # 启动MQTT客户端
    print("\n3. 启动MQTT客户端...")
    print("注意: 程序将持续运行，按 Ctrl+C 停止")
    print("如果程序立即退出，请检查网络连接和MQTT broker配置")
    print("-" * 50)
    
    try:
        # 运行主程序
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except subprocess.CalledProcessError as e:
        print(f"\n程序执行失败，退出码: {e.returncode}")
        return False
    
    return True

def check_network_connectivity():
    """检查网络连接"""
    print("\n4. 检查网络连接...")
    import config
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((config.MQTT_BROKER, config.MQTT_PORT))
        sock.close()
        
        if result == 0:
            print(f"✓ 可以连接到 {config.MQTT_BROKER}:{config.MQTT_PORT}")
            return True
        else:
            print(f"✗ 无法连接到 {config.MQTT_BROKER}:{config.MQTT_PORT}")
            return False
    except Exception as e:
        print(f"✗ 网络连接检查失败: {e}")
        return False

if __name__ == "__main__":
    print("开始MQTT客户端测试...")
    
    # 检查网络连接
    if not check_network_connectivity():
        print("\n建议检查:")
        print("1. 网络连接是否正常")
        print("2. MQTT broker地址和端口是否正确")
        print("3. 防火墙设置")
        sys.exit(1)
    
    # 运行测试
    success = test_mqtt_client()
    
    if success:
        print("\n测试完成")
    else:
        print("\n测试失败")
        sys.exit(1)