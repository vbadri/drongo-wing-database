import logging

from wing_module import Module


class Database(Module):
    # Database types
    MONGO = 'mongo'
    MYSQL = 'mysql'
    REDIS = 'redis'

    logger = logging.getLogger('wing_database')

    def init(self, app, config):
        self.logger.info('config : '.format(config))
        self.logger.info('Initializing [database] module with id {}.'.format(config.get('_id')))

        setattr(
            self.app.context.modules.database,
            config.get('_id'),
            self
        )

        self._type = config.get('type')
        if self._type == self.MONGO:
            from .databases._mongo import MongoDatabase
            klass = MongoDatabase

        elif self._type == self.REDIS:
            from .databases._redis import RedisDatabase
            klass = RedisDatabase

        elif self._type == self.MYSQL:
            from .databases._mysql import MysqlDatabase
            klass = MysqlDatabase

        else:
            self.logger.error('Unknown database type!')
            raise NotImplementedError

        self._inst = klass(self.app, config)

        self.logger.info(
            'Initialized database [{name}] of type [{type}]'.format(
                name=config._id,
                type=config.type
            )
        )

    @property
    def type(self):
        return self._type

    @property
    def instance(self):
        return self._inst
