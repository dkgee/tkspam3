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
channel.queue_declare(queue=queue_name)  # 如果队列没有创建，就创建这个队列

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    # import time
    # time.sleep(10)
    # print('ok')
    ch.basic_ack(delivery_tag=method.delivery_tag)

# no_ack
channel.basic_consume(callback, queue=queue_name, no_ack=False)
print(' [*] Waiting for message. To exit press CTRL+C')
channel.start_consuming()

