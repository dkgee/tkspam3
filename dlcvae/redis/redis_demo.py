# -*- coding: utf-8 -*-

import redis

# r = redis.Redis(host='172.30.154.242', port=7001)
# r.set('name','tk')
# print(r.get('name'))

# pool = redis.ConnectionPool(host='172.30.154.242', port=7001)
# r = redis.Redis(connection_pool=pool)

# 1,键值对方式
# r.set('name', 'jht')
# print(r.get('name').decode())      #解码redis中的字节值
# 2,管道方式(一次执行多个命令)
# pipe = r.pipeline(transaction=True)
# r.set('name', 'tk')
# r.set('name', 'xiaoqiang')
# pipe.execute()
# print(r.get('name').decode())
# print(r.get('second').decode())

# 3，发布和订阅
class RedisHelper(object):
    def __init__(self):
        self.__conn = redis.Redis(host='172.30.154.242', port=7001)
        self.channel = 'monitor'

    def publish(self, msg):
        self.__conn.publish(self.channel, msg)
        return True

    def subscribe(self):
        pub = self.__conn.pubsub()
        pub.subscribe(self.channel)
        pub.parse_response()
        return pub

obj = RedisHelper()
# obj.publish('hello') # 发布

#订阅
redis_sub = obj.subscribe()
while True:
    msg = redis_sub.parse_response()
    print(msg[2].decode())



# redis 单兵哨卫模式
# from redis.sentinel import Sentinel
# sentinel = Sentinel([('172.30.154.242', 7001),('172.30.154.242', 7002)], socket_timeout=0.1)

# redis 集群连接模式
# from rediscluster