from argparse import ArgumentParser
from subprocess import (Popen, PIPE)


PROJECT_PREFIX = '@'


class GitError(Exception):
    pass


def parse_args():
    parser = ArgumentParser(description='git-projects')
    parser.add_argument(PROJECT_PREFIX, nargs='+', help='project name')
    return parser.parse_known_args()


def parse_command():
    args, ignored_args = parse_args()
    args = args.__dict__.get(PROJECT_PREFIX)

    projects = list()
    git_args = list()

    for arg in args:
        if str.startswith(arg, PROJECT_PREFIX):
            projects.append(arg)
        else:
            git_args.append(arg)

    for i in range(len(projects)):
        projects[i] = projects[i][1:]

    return projects, git_args + ignored_args


def git(target, *args):
    """
    Git command opener wrapper.
    """
    cmd = ['git'] + list(args)
    popen = Popen(cmd, close_fds=True, cwd=target,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = popen.communicate()
    if popen.returncode != 0:
        raise GitError(err)
    return out