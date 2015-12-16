# from datetime import datetime
import datetime
import pony.orm as pny
import abc
from pony.orm.ormtypes import LongStr
from biomio.constants import REDIS_USER_KEY, REDIS_EMAILS_KEY, REDIS_APPLICATION_KEY, MYSQL_APPS_TABLE_NAME, \
    MYSQL_EMAILS_TABLE_NAME, MYSQL_USERS_TABLE_NAME, MYSQL_TRAINING_DATA_TABLE_NAME, MYSQL_CHANGES_TABLE_NAME, \
    MYSQL_POLICIES_TABLE_NAME, REDIS_USER_POLICY_KEY, MYSQL_DEVICE_INFORMATION_TABLE_NAME, REDIS_DEVICE_INFORMATION_KEY, \
    MYSQL_PGP_KEYS_TABLE_NAME, REDIS_PGP_DATA_KEY
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

    @staticmethod
    @abc.abstractmethod
    def update_record(record_id, **kwargs):
        """
            Updates record inside current table
        :param record_id: record to update
        :param kwargs: param/value dictionary
        """

    @staticmethod
    @abc.abstractmethod
    def get_table_name():
        """
            Returns MySQL table name of the current entity.

        :return: str MySQL table name
        """
        return


class UserInformation(BaseEntityClass, database.Entity):
    _table_ = MYSQL_USERS_TABLE_NAME
    id = pny.PrimaryKey(int, auto=True)
    api_id = pny.Required(int, default=1, lazy=True)
    name = pny.Required(str, 50, default='test_name', lazy=True)
    emails = pny.Set('PgpKeysData')
    phones = pny.Optional(str, 255, default='[]', lazy=True)
    password = pny.Required(str, 50, default='test_pass', lazy=True)
    temp_pass = pny.Optional(str, 50, default='test_temp_pass', lazy=True)
    type = pny.Required(str, 50, default='USER', sql_type="enum('ADMIN','USER','PROVIDER','PARTNER')", lazy=True)
    acc_type = pny.Required(bool, default=True, lazy=True)
    creation_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    last_login_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), auto=True, lazy=True)
    last_ip = pny.Required(str, 20, default='127.0.0.1', auto=True, lazy=True)
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

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_USERS_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        pass


class Email(BaseEntityClass, database.Entity):
    _table_ = MYSQL_EMAILS_TABLE_NAME
    profileId = pny.Required(int)
    email = pny.Required(str)
    verified = pny.Optional(bool, default=False)
    primary = pny.Optional(bool, default=False)
    extension = pny.Optional(bool, default=False)
    dateCreated = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)

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
        pass

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_EMAILS_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        pass


class PgpKeysData(BaseEntityClass, database.Entity):
    _table_ = MYSQL_PGP_KEYS_TABLE_NAME
    email = pny.PrimaryKey(str, auto=False)
    pass_phrase = pny.Optional(str)
    public_pgp_key = pny.Optional(LongStr, lazy=False)
    private_pgp_key = pny.Optional(LongStr, lazy=False, nullable=True)
    user = pny.Required(UserInformation)

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return REDIS_PGP_DATA_KEY % self.email

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
        PgpKeysData(**kwargs)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_PGP_KEYS_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        search_query = {PgpKeysData.get_unique_search_attribute(): record_id}
        email_data = PgpKeysData.get(**search_query)

        for key, value in kwargs.iteritems():
            if not hasattr(email_data, key):
                continue
            setattr(email_data, key, value)


class Application(BaseEntityClass, database.Entity):
    _table_ = MYSQL_APPS_TABLE_NAME
    app_id = pny.PrimaryKey(str, auto=False)
    app_type = pny.Required(str, sql_type="enum('extension', 'probe')")
    public_key = pny.Required(LongStr, lazy=False)
    users = pny.Set(UserInformation)

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
        if 'users' in kwargs and isinstance(kwargs.get('users'), (int, long, str)):
            search_query = {UserInformation.get_unique_search_attribute(): kwargs.get('users')}
            user = UserInformation.get(**search_query)
            kwargs.update({'users': [user]})
        Application(**kwargs)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_APPS_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        search_query = {Application.get_unique_search_attribute(): record_id}
        application = Application.get(**search_query)

        for key, value in kwargs.iteritems():
            if not hasattr(application, key):
                continue
            if key == 'users':
                for user_id in value:
                    if isinstance(user_id, UserInformation):
                        application.users.add(user_id)
                    else:
                        search_query = {UserInformation.get_unique_search_attribute(): user_id}
                        user = UserInformation.get(**search_query)
                        application.users.add(user)
            else:
                setattr(application, key, value)


class ChangesTable(BaseEntityClass, database.Entity):
    _table_ = MYSQL_CHANGES_TABLE_NAME
    table_name = pny.Required(str)
    record_id = pny.Optional(str)
    change_time = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now())
    # pny.composite_key(table_name, record_id)

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

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_CHANGES_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        pass


class TrainingData(BaseEntityClass, database.Entity):
    _table_ = MYSQL_TRAINING_DATA_TABLE_NAME
    probe_id = pny.PrimaryKey(str, auto=False)
    data = pny.Required(LongStr, lazy=False)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        TrainingData(**kwargs)

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return ''

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'probe_id'

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_TRAINING_DATA_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        search_query = {TrainingData.get_unique_search_attribute(): record_id}
        training_data = TrainingData.get(**search_query)

        for key, value in kwargs.iteritems():
            if not hasattr(training_data, key):
                continue
            setattr(training_data, key, value)


class Policy(BaseEntityClass, database.Entity):
    _table_ = MYSQL_POLICIES_TABLE_NAME
    owner = pny.Required(int, unique=True)
    name = pny.Required(str, default='No name')
    bioAuth = pny.Optional(str)
    minAuth = pny.Required(int, default=0)
    maxAuth = pny.Required(int, default=0)
    matchCertainty = pny.Required(int, default=0)
    geoRestriction = pny.Optional(str)
    timeRestriction = pny.Optional(str)
    dateCreated = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    dateModified = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), auto=True, lazy=True)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_POLICIES_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        Policy(**kwargs)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        search_query = {Policy.get_unique_search_attribute(): record_id}
        policy_data = Policy.get(**search_query)

        for key, value in kwargs.iteritems():
            if not hasattr(policy_data, key):
                continue
            setattr(policy_data, key, value)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'owner'

    @inherit_docstring_from
    def get_redis_key(self):
        return REDIS_USER_POLICY_KEY % self.owner


class DeviceInformation(BaseEntityClass, database.Entity):
    _table_ = MYSQL_DEVICE_INFORMATION_TABLE_NAME
    profileId = pny.Required(int)
    serviceId = pny.Required(int)
    title = pny.Optional(str, default='No_name')
    status = pny.Optional(bool, default=0)
    device_token = pny.Optional(str)
    push_token = pny.Optional(str)
    date_created = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), lazy=True)
    date_modified = pny.Required(datetime.datetime, default=lambda: datetime.datetime.now(), auto=True, lazy=True)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_table_name():
        return MYSQL_DEVICE_INFORMATION_TABLE_NAME

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def create_record(**kwargs):
        DeviceInformation(**kwargs)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def update_record(record_id, **kwargs):
        search_query = {DeviceInformation.get_unique_search_attribute(): record_id}
        device_information = DeviceInformation.get(**search_query)
        if device_information is not None:
            for key, value in kwargs.iteritems():
                if not hasattr(device_information, key):
                    continue
                setattr(device_information, key, value)

    @staticmethod
    @inherit_docstring_from(BaseEntityClass)
    def get_unique_search_attribute():
        return 'device_token'

    @inherit_docstring_from(BaseEntityClass)
    def get_redis_key(self):
        return REDIS_DEVICE_INFORMATION_KEY % self.device_token
