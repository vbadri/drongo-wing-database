import pymysql
import pymysql.cursors


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 3306
DEFAULT_CHARSET = 'utf8'


class MysqlDatabase(object):
    def __init__(self, app, **kwargs):
        host = kwargs.get('host', DEFAULT_HOST)
        port = kwargs.get('port', DEFAULT_PORT)
        user = kwargs.get('user')
        password = kwargs.get('password')
        name = kwargs.get('name')
        charset = kwargs.get('charset', DEFAULT_CHARSET)

        self.connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=name,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )

    def get(self):
        return self.connection
