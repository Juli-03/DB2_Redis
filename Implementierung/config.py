import redis

class Config(object):
    # connection to redis db
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    redis = redis.Redis(connection_pool=pool)