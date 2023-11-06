import redis



class Config(object):
    # connection to redis db
    host = 'localhost' # ip address of redis server or localhost
    port = 6379 #port for redis server (default: 6379)

    pool = redis.ConnectionPool(host=host, port=port, db=0)
    redis = redis.Redis(connection_pool=pool)

