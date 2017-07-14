MONGO = 'mongo'
REDIS = 'redis'


class Database(object):
    def __init__(self, app, **kwargs):
        if kwargs.get('type') == MONGO:
            from .databases._mongo import MongoDatabase
            self._inst = MongoDatabase(app, **kwargs)
        elif kwargs.get('type') == REDIS:
            from .databases._redis import RedisDatabase
            self._inst = RedisDatabase(app, **kwargs)

    @property
    def instance(self):
        return self._inst
