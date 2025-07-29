#!/bin/bash

# Install prerequisites
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv git

# Create project directory
sudo mkdir -p /srv/mqtt-sub-svc
sudo chown $(whoami):$(whoami) /srv/mqtt-sub-svc
cd /srv/mqtt-sub-svc

# Clone repository
git clone https://github.com/kronecai/mqtt-sub-svc.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create log file path
sudo mkdir /var/log/mqtt-sub-svc
sudo chown $(whoami) /var/log/mqtt-sub-svc
sudo chmod 755 /var/log/mqtt-sub-svc/

# Create systemd service
sudo tee /etc/systemd/system/mqtt-sub-svc.service <<EOF
[Unit]
Description=MQTT Subscription Service
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=/srv/mqtt-sub-svc
Environment="PATH=/srv/mqtt-sub-svc/venv/bin"
ExecStart=/srv/mqtt-sub-svc/venv/bin/python /srv/mqtt-sub-svc/mqtt-sub-svc/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload and enable service
sudo systemctl daemon-reload
sudo systemctl enable mqtt-sub-svc.service
sudo systemctl start mqtt-sub-svc.service

echo "Deployment completed!"