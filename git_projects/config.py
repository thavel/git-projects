from os import listdir
from os.path import expanduser, join, split as split_path

from yaml import load


class ConfigError(Exception):
    pass


class Target(object):
    """
    Object representation of a repository targeted by git-project
    """
    def __init__(self, path, repo, origin):
        clean_repo = Target.clean_path(repo)
        if path is not None:
            self.name = clean_repo
            self.path = join(path, self.name)
        else:
            self.path = clean_repo
            self.name = split_path(self.path)[1]
        self.origin = origin

    @property
    def root(self):
        return split_path(self.path)[0]

    @classmethod
    def clean_path(cls, path):
        path = expanduser(path)
        return path[:-1] if path[-1:] is '/' else path

    def __hash__(self):
        return hash(self.path)

    def __eq__(self, other):
        return self.path == other.path


class ConfigParser(object):

    def __init__(self, file_path):
        self.file_path = expanduser(file_path)
        self.config = self.parse(self.file_path)

    @staticmethod
    def parse(file_path):
        with open(file_path, 'r') as file_content:
            return load(file_content)

    @property
    def projects(self):
        """
        Gives the list of projects.
        """
        return self.config.keys()

    def path(self, project):
        """
        Gives the path attribute for a specific project.
        """
        path = self.config[project].get('path', None)

        if not path:
            return
        return expanduser(path)

    def origin(self, project):
        """
        Gives the origin attribute for a specific project.
        """
        return self.config[project].get('origin', None)

    def repositories(self, project):
        """
        Gives the list of repositories for a specific project.
        """
        return self.config[project].get('repositories', [])

    def subprojects(self, project):
        """
        Gives the list of sub-projects for a specific project.
        """
        return self.config[project].get('subprojects', [])

    def validation(self, project):
        """
        Check if the project description is valid.
        """
        # The project exists
        if project not in self.config:
            raise ConfigError("Project {} doesn't exist".format(project))

        path = self.path(project)
        repos = self.repositories(project)
        subproj = self.subprojects(project)

        # At least one of the parameter is defined
        if not (path or repos or subproj):
            raise ConfigError("Empty project {}".format(project))

        # Check all sub-projects
        for proj in subproj:
            if proj not in self.projects:
                raise ConfigError("Sub-project {} isn't defined".format(proj))
            self.validation(proj)

    def directories(self, project):
        """
        Gives the list of directories targeted by a project
        """
        self.validation(project)

        path = self.path(project)
        repos = self.repositories(project)
        subproj = self.subprojects(project)
        origin = self.origin(project)

        targets = list()
        if path and not repos:
            repos = list(filter(lambda i: '.' not in i, listdir(path)))

        for repo in repos:
            target = Target(path, repo, origin)
            targets.append(target)

        for proj in subproj:
            subtargets = self.directories(proj)
            # Inherit origin from higher project if empty
            for target in subtargets:
                target.origin = target.origin or origin
            targets += subtargets

        return targets
