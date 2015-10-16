from enum import Enum


class Format(Enum):
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def bold(message):
    return Format.BOLD.value + message + Format.END.value


def warning(message):
    return Format.RED.value + message + Format.END.value


def info(message):
    return Format.YELLOW.value + message + Format.END.value


def success(message):
    return Format.GREEN.value + message + Format.END.value
