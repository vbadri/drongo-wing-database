from wing_module import Module


class Database(Module):
    # Database types
    MONGO = 'mongo'
    MYSQL = 'mysql'
    REDIS = 'redis'

    def init(self, config):
        self._type = config.get('type')
        if self._type == self.MONGO:
            from .databases._mongo import MongoDatabase
            self._inst = MongoDatabase(self.app, **config)

        elif self._type == self.REDIS:
            from .databases._redis import RedisDatabase
            self._inst = RedisDatabase(self.app, **config)

        elif self._type == self.MYSQL:
            from .databases._mysql import MysqlDatabase
            self._inst = MysqlDatabase(self.app, **config)

    @property
    def type(self):
        return self._type

    @property
    def instance(self):
        return self._inst
