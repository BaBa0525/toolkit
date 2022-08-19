def static_vars(**kwargs):
    """
    Adding static-variable-like attributes to functions.

    Those "static variables" can be accessed through `funcName.attrName`.

    Args:
        **kwargs: Arbitrary names with the initial value as needed.
    """

    def wrapper(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return wrapper
