from wing_module import Module

import logging


class Database(Module):
    # Database types
    MONGO = 'mongo'
    MYSQL = 'mysql'
    REDIS = 'redis'

    logger = logging.getLogger('wing_database')

    def init(self, config):
        self.logger.info('Initializing [database] module.')

        setattr(
            self.app.context.modules.database,
            config.get('_id'),
            self
        )

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
