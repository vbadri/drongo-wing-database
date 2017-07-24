MONGO = 'mongo'
MYSQL = 'mysql'
REDIS = 'redis'


class Database(object):
    def __init__(self, app, **kwargs):
        if kwargs.get('type') == MONGO:
            from .databases._mongo import MongoDatabase
            self._inst = MongoDatabase(app, **kwargs)
        elif kwargs.get('type') == REDIS:
            from .databases._redis import RedisDatabase
            self._inst = RedisDatabase(app, **kwargs)
        elif kwargs.get('type') == MYSQL:
            from .databases._mysql import MysqlDatabase
            self._inst = MysqlDatabase(app, **kwargs)

    @property
    def instance(self):
        return self._inst
