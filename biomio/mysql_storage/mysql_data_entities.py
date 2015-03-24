# from datetime import datetime
import pony.orm as pny
import abc
from biomio.constants import REDIS_USER_KEY, REDIS_SESSION_KEY, REDIS_APPLICATION_KEY

database = pny.Database()


class BaseEntityClass(object):
    # create_date = pny.Required(datetime, sql_default='CURRENT_TIMESTAMP')

    @staticmethod
    @abc.abstractmethod
    def get_redis_key(key_value):
        """
            Returns Redis key for current table type.
        :param key_value: Value that is used to generate the redis key.
        :return: str redis key.

        """
        return

    @staticmethod
    @abc.abstractmethod
    def get_unique_search_attribute():
        """
            Returns default unique search attribute for current table type.
        :return: str unique attribute.

        """
        return

    @staticmethod
    @abc.abstractmethod
    def create_record(**kwargs):
        """
            Creates record inside current table.
        :param kwargs: param/value dictionary.
        """


class UserInformation(BaseEntityClass, database.Entity):
    user_id = pny.Required(str, unique=True)
    name = pny.Optional(str, nullable=True)

    @staticmethod
    def get_redis_key(user_id):
        return REDIS_USER_KEY % user_id

    @staticmethod
    def get_unique_search_attribute():
        return 'user_id'

    @staticmethod
    def create_record(**kwargs):
        UserInformation(**kwargs)


class EmailPGPInformation(BaseEntityClass, database.Entity):
    email = pny.Required(str, unique=True)
    pass_phrase = pny.Required(str)
    public_pgp_key = pny.Required(str)
    private_pgp_key = pny.Optional(str, nullable=True)

    @staticmethod
    def get_redis_key(email):
        return 'user_email:%s' % email

    @staticmethod
    def get_unique_search_attribute():
        return 'email'

    @staticmethod
    def create_record(**kwargs):
        if 'user' in kwargs:
            search_query = {UserInformation.get_unique_search_attribute(): kwargs.get('user')}
            user = UserInformation.get(**search_query)
            kwargs.update({'user': user})
        EmailPGPInformation(**kwargs)


class AppInformation(BaseEntityClass, database.Entity):
    app_id = pny.Required(str, unique=True)
    public_key = pny.Required(str)

    @staticmethod
    def get_redis_key(app_id):
        return REDIS_APPLICATION_KEY % app_id

    @staticmethod
    def get_unique_search_attribute():
        return 'app_id'

    @staticmethod
    def create_record(**kwargs):
        if 'users' in kwargs:
            search_query = {UserInformation.get_unique_search_attribute(): kwargs.get('users')}
            user = UserInformation.get(**search_query)
            kwargs.update({'users': [user]})
        AppInformation(**kwargs)


class ChangesTable(BaseEntityClass, database.Entity):
    table_name = pny.Required(str)
    object_id = pny.Required(str)

    pny.composite_key(table_name, object_id)

    @staticmethod
    def create_record(**kwargs):
        ChangesTable(**kwargs)

    @staticmethod
    def get_redis_key(key_value):
        return ''

    @staticmethod
    def get_unique_search_attribute():
        return 'redis_key'


class SessionData(BaseEntityClass, database.Entity):
    refresh_token = pny.Required(str)
    state = pny.Required(str)
    ttl = pny.Optional(int)

    pny.composite_key(refresh_token, state)

    @staticmethod
    def get_redis_key(refresh_token):
        return REDIS_SESSION_KEY % refresh_token

    @staticmethod
    def get_unique_search_attribute():
        return 'refresh_token'

    @staticmethod
    def create_record(**kwargs):
        SessionData(**kwargs)
