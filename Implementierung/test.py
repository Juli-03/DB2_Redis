import redis


pool = redis.ConnectionPool(host='141.31.94.106', port=6379, db=0)
redis = redis.Redis(connection_pool=pool)

#redis.set('wohnort', 'kölle')
value = redis.get('lieblingstier')
print(value)

#redis.zadd('vehicles', {'car' : 0})
#redis.zadd('vehicles', {'bike' : 0})
#vehicles = redis.zrange('vehicles', 0, -1)
#print(vehicles)