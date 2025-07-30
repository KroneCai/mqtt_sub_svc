module.exports = {
  apps: [
    // mqtt后台订阅服务
    {
    name: "mqtt-sub-svc",
    script: "/Users/kronecai/project/mqtt_sub_svc/mqtt-sub-svc/main.py", // 脚本路径
    interpreter: "/Users/kronecai/project/mqtt_sub_svc/venv/bin/python3",  // 虚拟环境解释器
    cwd: "/Users/kronecai/project/mqtt_sub_svc",                   // 工作目录
    autorestart: true,                         // 自动重启
    }]
    
};