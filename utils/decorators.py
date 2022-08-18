def static_vars(**kwargs):
    """
    Adding static-variable-like attributes to functions.

    Those "static variables" can be accessed through `funcName.attrName`.
    """

    def wrapper(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return wrapper
