import sys


def inline_print(msg):
    sys.stdout.write(msg)
    sys.stdout.flush()


def pipe_lines(msg):
    if not msg:
        return ''
    return '| ' + msg.replace('\n', '\n| ')[:-2] + '\n'


class Format(object):
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
    return Format.BOLD + message + Format.END


def error(message):
    return Format.RED + message + Format.END


def warning(message):
    return Format.YELLOW + message + Format.END


def info(message):
    return Format.BLUE + message + Format.END


def success(message):
    return Format.GREEN + message + Format.END
