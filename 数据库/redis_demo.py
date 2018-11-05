"""
Redis 是 StrictRedis 的子类, 推荐使用 StrictRedis
StrictRedis 是 Redis 的子类, 推荐使用 StrictRedis
date: 18-9-27 下午6:14
"""
import redis

# redis = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
"""
host: 地址
port: 端口
password: 密码
db: 数据库index
decode_responses: 是否解码返回
"""
# 连接数据库
redis = redis.StrictRedis(host="127.0.0.1", port=6379, password="123456", db=0, decode_responses=True)
redis.set("name", "lnsist")
print(redis.get("name"))

# 连接池, 不做任何真实的redis连接, 仅仅是设置最大连接数, 连接参数和连接类, 切换后也不会进行释放
pool_0 = redis.ConnectionPool(host='localhost', port=6379, password="123456", db=0, decode_responses=True)
pool_1 = redis.ConnectionPool(host='localhost', port=6379, password="123456", db=1, decode_responses=True)
pool_2 = redis.ConnectionPool(host='localhost', port=6379, password="123456", db=2, decode_responses=True)
pool_10 = redis.ConnectionPool(host='localhost', port=6379, password="123456", db=10, decode_responses=True)
# 当需要调用某个具体的数据库才去调用相应的连接池, 减少新建和释放的资源
r = redis.Redis(connection_pool=pool_10)
# gender 取出键male对应的值
print(r.get('zidingyi'))
