import pony.orm as pny

database = pny.Database()
pny.sql_debug(True)


class Test1(database.Entity):
    name = pny.Required(str)
    value = pny.Required(int)


class Test2(database.Entity):
    name = pny.Required(str)
    value = pny.Required(str)
