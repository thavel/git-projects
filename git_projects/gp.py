#!/usr/bin/env python

from os.path import split

from git_projects.config import ConfigParser, ConfigError
from git_projects.console import success, info, warning, error, bold
from git_projects.command import parse_command, git, GitError
from yaml.error import YAMLError


CONFIG_FILE = '~/.gitprojects'


def fail(msg=None, exc=None):
    message = msg or str()
    if exc:
        message = "{}: {}".format(message, str(exc))
    if not message:
        message = "Unknown error"

    print(error(message))
    exit(1)


def main():
    # Configuration parsing
    config = None
    try:
        config = ConfigParser(CONFIG_FILE)
    except EnvironmentError:
        fail("Configuration file {} is missing".format(CONFIG_FILE))
    except YAMLError as e:
        fail(exc=e)

    # Command parsing
    projects, git_args = parse_command()
    targets = list()
    for project in projects:
        try:
            targets += config.directories(project)
        except ConfigError as exc:
            fail(exc=e)

    # Command execution in all targets
    for target in set(targets):
        name = split(target)[1]
        print(bold("Repository candidate: ") + info(name))

        try:
            git(*git_args)
        except GitError as exc:
            print(info(str(exc)))


if __name__ == "__main__":
    main()
