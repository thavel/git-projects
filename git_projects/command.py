from argparse import ArgumentParser


PROJECT_PREFIX = '@'


def parse_args():
    parser = ArgumentParser(description='git-projects')
    parser.add_argument(PROJECT_PREFIX, nargs='+', help='project name')
    return parser.parse_args()


def parse_command():
    args = parse_args().__dict__.get(PROJECT_PREFIX)

    projects = list()
    git_args = list()

    for arg in args:
        if str.startswith(arg, PROJECT_PREFIX):
            projects.append(arg)
        else:
            git_args.append(arg)

    for i in range(len(projects)):
        projects[i] = projects[i][1:]

    return projects, git_args
