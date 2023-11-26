import redis
import time
from config import Config
import lorem

# connection to database
pool = Config.pool
redis = Config.redis



start_time = time.time()
end_time = start_time + 10 # start time + 10 seconds
message_counter = 0
while time.time() < end_time:   
    # get random generated text
    # add to redis sorted set
    message_counter += 1
    message = str(lorem.sentence())
    redis.zadd("performance_test", {message:message_counter})
print(message_counter)

