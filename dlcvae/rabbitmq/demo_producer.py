# -*- coding: utf-8 -*-

import pika

host_ip ="172.30.154.241"
uport="8101"
uuser="admin"
upass="123456"
virtual_host="/"

credentials = pika.PlainCredentials(uuser, upass)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_ip,port=uport,virtual_host=virtual_host, credentials=credentials))
channel = connection.channel()
queue_name = 'site:tool:trace'
while True:
    channel.basic_publish(exchange='', routing_key=queue_name, body='Hello World!')
    print(" [x] Send 'Hello World!'")
connection.close()