from functools import wraps

from exceptions import ContactDoesNotExist, ValidationError


def input_error(usage):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValidationError, ContactDoesNotExist) as error:
                return str(error)
            except (ValueError, IndexError):
                return f"Usage: {usage}"
            except KeyError as error:
                return f"Contact '{error.args[0]}' not found."

        return inner

    return decorator
