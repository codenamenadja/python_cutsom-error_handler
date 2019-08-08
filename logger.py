from logging import Logger, Formatter, FATAL, DEBUG, FileHandler, StreamHandler, ERROR
from typing import Optional


def _get_formatter() -> Formatter:
    formatter: Formatter
    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return formatter


def _add_file_hanlder_for_all(logger: Logger, formatter: Formatter) -> Logger:
    fh: FileHandler
    fh = FileHandler(
        f"debug_{logger.name}.log") if logger.name else FileHandler("debug.log")
    fh.setLevel(DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def _add_stream_hanlder_for_error(logger: Logger, formatter: Formatter) -> Logger:
    ch: StreamHandler
    ch = StreamHandler()
    ch.setLevel(ERROR)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def log_to_csv(logger_name: Optional[str] = "unexpected") -> bool:
    import csv
    from os.path import curdir, abspath, exists, join, isfile
    filename = f"debug_{logger_name}"
    print(filename)
    debugfile = join(curdir, f"{filename}.log")
    csvfile = join(curdir, f"{filename}.csv")
    condition_debugfile = exists(debugfile) and isfile(debugfile)
    if not condition_debugfile:
        return False
    with open(debugfile, "r", encoding="latin-1") as log:
        keys = ["asctime", "name", "level", "filename",
                "lineno", "message", ]
        with open(csvfile, "w") as newfile:
            writer = csv.DictWriter(newfile, keys)
            writer.writeheader()
            while True:
                line = log.readline()
                if not line:
                    break
                data_as_dict = dict(zip(keys, line.split(" - ")))
                writer.writerow(data_as_dict)
                return True


def get_debug_logger(expected=False, formatter: Formatter = _get_formatter()) -> Logger:
    logger: Logger
    if expected:
        logger = Logger("expected")
        logger.setLevel(DEBUG)
    else:
        logger = Logger("unexpected")
        logger.setLevel(FATAL)
    streamhandled_logger: Logger = _add_stream_hanlder_for_error(
        logger, formatter)
    filehandled_logger: Logger = _add_file_hanlder_for_all(
        streamhandled_logger, formatter)
    return filehandled_logger

    if __name__ == "__main__":
        logger = get_debug_logger("normal")
