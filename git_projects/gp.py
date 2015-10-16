#!/usr/bin/env python

from git_projects.config import ConfigParser, ConfigError
from git_projects.console import warning
from yaml.error import YAMLError


CONFIG_FILE = '~/.gitprojects'

try:
    config = ConfigParser(CONFIG_FILE)
except FileNotFoundError:
    print(warning("Configuration file {} is missing").format(CONFIG_FILE))
    exit(1)
except YAMLError as e:
    print(warning(str(e)))
    exit(1)


def main():
    try:
        print(config.directories('wings'))
    except ConfigError as e:
        print(warning(str(e)))


if __name__ == "__main__":
    main()
