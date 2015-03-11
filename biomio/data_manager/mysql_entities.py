import pony.orm as pny

database = pny.Database()
pny.sql_debug(True)


class UserInformation(database.Entity):
    user_id = pny.Required(str, unique=True)
    name = pny.Optional(str, nullable=True)
    emails = pny.Set('EmailPGPInformation')
    applications = pny.Set('AppInformation')

    @staticmethod
    def get_redis_key(user_id):
        return 'user:%s' % user_id

    @staticmethod
    def get_unique_search_query(search_param):
        return {'user_id': search_param}

    @staticmethod
    def create_record(**kwargs):
        UserInformation(**kwargs)


class EmailPGPInformation(database.Entity):
    email = pny.Required(str, unique=True)
    pass_phrase = pny.Required(str)
    public_pgp_key = pny.Required(str)
    private_pgp_key = pny.Optional(str, nullable=True)
    user = pny.Required(UserInformation)

    @staticmethod
    def get_redis_key(email):
        return 'user_email:%s' % email

    @staticmethod
    def get_unique_search_query(search_param):
        return {'email': search_param}

    @staticmethod
    def create_record(**kwargs):
        if 'user' in kwargs:
            search_query = UserInformation.get_unique_search_query(kwargs.get('user'))
            user = UserInformation.get(**search_query)
            print "============="
            print user
            print "============="
            kwargs.update({'user': user})
        EmailPGPInformation(**kwargs)


class AppInformation(database.Entity):
    app_id = pny.Required(str, unique=True)
    app_public_key = pny.Required(str)
    users = pny.Set(UserInformation)

    @staticmethod
    def get_redis_key(app_id):
        return 'acount:%s:%s' % ('id', app_id)

    @staticmethod
    def get_unique_search_query(search_param):
        return {'app_id': search_param}

    @staticmethod
    def create_record(**kwargs):
        print kwargs
        if 'users' in kwargs:
            search_query = UserInformation.get_unique_search_query(kwargs.get('users'))
            user = UserInformation.get(**search_query)
            print "============="
            print user
            print "============="
            kwargs.update({'users': [user]})
        AppInformation(**kwargs)


class ChangesTable(database.Entity):
    redis_key = pny.Required(str, unique=True)

    @staticmethod
    def create_record(**kwargs):
        ChangesTable(**kwargs)