#!/usr/bin/env python

import os
from yaml.error import YAMLError
from git_projects.shortcut import ShortcutHolder
from git_projects.command import parse_command, git, GitError
from git_projects.config import ConfigParser, ConfigError, PathError
from git_projects.console import (inline_print, pipe_lines,
                                  info, error, success, warning, bold)


CONFIG_FILE = '~/.gitprojects'


def fail(msg=None, exc=None):
    message = msg or str()
    if not message:
        message = "Error"
    if exc:
        message = "{}: {}".format(message, str(exc))

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
    projects, git_args, shortcuts = parse_command()
    targets = list()
    for project in projects:
        try:
            targets += config.directories(project)
        except PathError as exc:
            origin = config.origin(project)
            missing = str(exc).split(',')
            for path in missing:
                # Clone the repository if it does not exist
                base, repo = os.path.split(path)
                if origin:
                    print(warning('Cloning {}...'.format(repo)))
                    git(base, 'clone', "{}/{}.git".format(origin, repo))
            targets += config.directories(project)
        except ConfigError as exc:
            fail(exc=exc)

    # Command-line validation
    shortcuts_use = sum(shortcuts.values())
    if shortcuts_use and git_args:
        fail("Please use shortcuts without argument")
    if not shortcuts_use and not git_args:
        fail("Nothing to do, bail out")
    if shortcuts_use > 1:
        fail("Only one shortcut is allowed per command")

    # Command execution in all targets
    for target in set(targets):
        repo_name = os.path.split(target)[1]
        inline_print(bold("Target repository: ") + info(repo_name))

        try:
            out = str()
            if shortcuts_use:
                # Select the shortcut
                name = {v: k for k, v in shortcuts.items()}[True]
                shortcut = ShortcutHolder.REGISTRY[name]
                # Execute all commands related to the shortcut
                for command in shortcut.commands():
                    out = git(target, *command)

                if not shortcut.output:
                    out = ''
            else:
                out = git(target, *git_args)

            print(" => {}".format(success('done')))
            inline_print(pipe_lines(out))
        except GitError as exc:
            out = str(exc)
            print(" => {}".format(warning('failed')))
            inline_print(warning(pipe_lines(out)))
        except FileNotFoundError:
            out = "No local git repository"
            print(" => {}".format(warning('missing')))
            inline_print(warning(pipe_lines(out)))


if __name__ == "__main__":
    main()
