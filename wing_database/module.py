class Database(object):
    # Database types
    MONGO = 'mongo'
    MYSQL = 'mysql'
    REDIS = 'redis'

    def __init__(self, app, **kwargs):
        self._type = kwargs.get('type')
        if self._type == self.MONGO:
            from .databases._mongo import MongoDatabase
            self._inst = MongoDatabase(app, **kwargs)

        elif self._type == self.REDIS:
            from .databases._redis import RedisDatabase
            self._inst = RedisDatabase(app, **kwargs)

        elif self._type == self.MYSQL:
            from .databases._mysql import MysqlDatabase
            self._inst = MysqlDatabase(app, **kwargs)

    @property
    def type(self):
        self._type

    @property
    def instance(self):
        return self._inst
