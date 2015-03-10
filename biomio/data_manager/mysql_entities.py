import pony.orm as pny

database = pny.Database()
pny.sql_debug(True)


class EmailPGPInformation(database.Entity):
    email = pny.Required(str, unique=True)
    pass_phrase = pny.Required(str)
    public_pgp_key = pny.Required(str)
    private_pgp_key = pny.Optional(str)

    @staticmethod
    def get_redis_key(email):
        return 'user_email:%s' % email


class UserInformation(database.Entity):
    user_id = pny.Required(str, unique=True)
    name = pny.Optional(str)
    emails = pny.Set(EmailPGPInformation)

    @staticmethod
    def get_redis_key(user_id):
        return 'user:%s' % user_id


class AppInformation(database.Entity):
    app_id = pny.Required(str, unique=True)
    app_public_key = pny.Required(str)
    users = pny.Set(UserInformation)

    @staticmethod
    def get_redis_key(app_id):
        return 'acount:%s:%s' % ('id', app_id)


class ChangesTable(database.Entity):
    redis_key = pny.Required(str, unique=True)