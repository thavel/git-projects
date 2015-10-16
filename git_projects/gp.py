#!/usr/bin/env python

from git_projects.config import ConfigParser, ConfigError
from git_projects.console import warning
from git_projects.command import parse_command
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
    projects, git_args = parse_command()
    targets = list()

    for project in projects:
        try:
            targets += config.directories(project)
        except ConfigError as exc:
            print(warning(str(exc)))
            exit(1)

    targets = set(targets)


if __name__ == "__main__":
    main()
