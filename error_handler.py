from functools import wraps
from logging import DEBUG
from typing import Callable, Optional


def base_error_hanlder(func: Callable) -> Callable:
    """raise Error as below
    Error(message:str, level:str)
    [info error debug fatal warning critical], one could be second argument.
    >>> raise ValueError("something wrong", "critical")
    # named expected logger -> log_to debug_expected.log
    >>> raise ValueError("somethong wrong2")
    # named unexpected logger -> log_to debug_unexpected.log -> log to csv

    Arguments:
        func {Callable} -- [wrapped function by error_handler]

    Returns:
        [SpecificError] -- [means, logged all-right]
        [None] -- [not logged, cause of error.args[1]. must not mismatch to logger level]
    """
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BaseException as e:
            _log_to_logger(e)
    return _wrapper


def _log_to_logger(error: BaseException) -> bool:
    from os.path import abspath, dirname
    from logger import get_debug_logger, log_to_csv
    import inspect
    tb = error.__traceback__
    filename = abspath(inspect.getfile(tb))
    lineno = tb.tb_lineno
    err_level = error.args[-1] if len(error.args) is 2 else None
    message = f"{filename} - {lineno} - {error.args[0]}"
    logger = get_debug_logger(
        expected=True) if err_level else get_debug_logger()
    if err_level in "critical.fatal".split("."):
        logger.critical(message)
    elif (err_level in "error.warning.info.debug".split(".")):
        logger.debug(message)
    else:
        logger.fatal(message)
        log_to_csv()
    return True


if __name__ == "__main__":
    @base_error_hanlder
    def sample():
        raise ValueError("sample message")
    sample()
