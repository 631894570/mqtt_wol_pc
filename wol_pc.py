import paho.mqtt.client as mqtt
import os

HOST = "bemfa.com"
PORT = 9501
# 巴法平台控制台获取的私钥
client_id = "*********"
# 开机命令  etherwake -i 网卡名 -b MAC地址
cmd1='etherwake -i *** -b *********'
# 关机命令   ssh 用户名@ip "shutdown -s -t 0
cmd2='ssh administrator@****** "shutdown -s -t 0"'
#连接并订阅
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("PC002")         # 订阅消息

#消息接收
def on_message(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))
    sw = str(msg.payload.decode('utf-8'))
    if sw == "on":
        os.system(cmd1)
    else:
        os.system(cmd2)

#订阅成功
def on_subscribe(client, userdata, mid, granted_qos):
    print("On Subscribed: qos = %d" % granted_qos)

# 失去连接
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection %s" % rc)


client = mqtt.Client(client_id)
client.username_pw_set("userName", "passwd")
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect
client.connect(HOST, PORT, 60)
client.loop_forever()
