"""
File: config.py
Author: Tim Steiner, Julian Bork, Felix Wilhelm, Marius Wergen
Date: October 13, 2023
Description: This class contains the configuration for the redis database.

Usage:
- Class Config: Contains the configuration for the redis database.

- configuration is used in all routes of the application

- host: ip address of redis server or localhost

- port: port for redis server (default: 6379)

- pool: connection pool for redis server

- redis: redis connection
"""

# imports of used libraries
import redis

# class for configuration
# connection to redis db
class Config(object):
    # connection to redis db
    host = '127.0.0.1' # ip address of redis server or localhost
    port = 6379 #port for redis server (default: 6379)

    pool = redis.ConnectionPool(host=host, port=port, db=0)
    redis = redis.Redis(connection_pool=pool)

