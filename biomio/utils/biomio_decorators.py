def inherit_docstring_from(cls):
    """
        Inherits doc string from parent class method.
    :param cls: Parent class with the method.
    :return:
    """

    def docstring_inheriting_decorator(fn):
        fn.__doc__ = getattr(cls, fn.__name__).__doc__
        return fn

    return docstring_inheriting_decorator