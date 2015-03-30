# from datetime import datetime
import datetime
import pony.orm as pny
import abc
from biomio.constants import REDIS_USER_KEY, REDIS_EMAILS_KEY, REDIS_APPLICATION_KEY
from biomio.utils.biomio_decorators import inherit_docstring_from

database = pny.Database()


class BaseEntityClass(object):
    # create_date = pny.Required(datetime, sql_default='CURRENT_TIMESTAMP')

    @abc.abstractmethod
    def get_redis_key(self):
        """
            Returns Redis key for current table type.
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
    _table_ = "Profiles"
    id = pny.PrimaryKey(int, auto=True)
    api_id = pny.Required(int, default=1)
    name = pny.Required(str, 50, default='test_name')
    emails = pny.Set('EmailsData')
    phones = pny.Optional(str, 255, default='[]')
    password = pny.Required(str, 50, default='test_pass')
    temp_pass = pny.Optional(str, 50, default='test_temp_pass')
    type = pny.Required(str, 50, default='USER', sql_type="enum('ADMIN','USER','PROVIDER','PARTNER')")
    acc_type = pny.Required(bool, default=True)
    creation_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now())
    last_login_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), auto=True)
    last_ip = pny.Required(str, 20, default='127.0.0.1', auto=True)
    applications = pny.Set('Application')

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return REDIS_USER_KEY % self.id

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'id'

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        UserInformation(**kwargs)


class EmailsData(BaseEntityClass, database.Entity):
    _table_ = 'EmailsData'
    email = pny.Required(str, unique=True)
    pass_phrase = pny.Required(str)
    public_pgp_key = pny.Required(str)
    private_pgp_key = pny.Optional(str, nullable=True)
    user = pny.Required(UserInformation)

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return REDIS_EMAILS_KEY % self.email

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'email'

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        if 'user' in kwargs:
            search_query = {UserInformation.get_unique_search_attribute(): kwargs.get('user')}
            user = UserInformation.get(**search_query)
            kwargs.update({'user': user})
        EmailsData(**kwargs)


class Application(BaseEntityClass, database.Entity):
    _table_ = 'Applications'
    app_id = pny.PrimaryKey(str, auto=False)
    app_type = pny.Required(str, sql_type="enum('extension', 'probe')")
    public_key = pny.Required(str)
    user = pny.Required(UserInformation)

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return REDIS_APPLICATION_KEY % self.app_id

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'app_id'

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        if 'user' in kwargs and isinstance(kwargs.get('user'), (int, long, str)):
            search_query = {UserInformation.get_unique_search_attribute(): kwargs.get('user')}
            user = UserInformation.get(**search_query)
            kwargs.update({'user': user})
        Application(**kwargs)


class ChangesTable(BaseEntityClass, database.Entity):
    table_name = pny.Required(str)
    object_id = pny.Required(str)

    pny.composite_key(table_name, object_id)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        ChangesTable(**kwargs)

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return ''

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'redis_key'
