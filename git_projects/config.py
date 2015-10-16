from os import listdir
from os.path import expanduser, exists, join

from yaml import load


class ConfigError(Exception):
    pass


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

        # The path shall be valid
        if path and not exists(path):
            raise ConfigError("Path does't exist: {}".format(path))

        # Repositories but not root path, these should be absolute paths
        if repos and not path:
            for repo in repos:
                if not exists(expanduser(repo)):
                    raise ConfigError("Path doesn't exist: {}".format(repo))

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

        dirs = list()

        if path and not repos:
            repos = list(filter(lambda i: '.' not in i, listdir(path)))

        for repo in repos:
            if path is not None:
                rpath = join(path, repo)
                if not exists(rpath):
                    raise ConfigError("Path doesn't exist: {}".format(rpath))
                dirs.append(rpath)
            else:
                dirs.append(expanduser(repo))

        for proj in subproj:
            dirs += self.directories(proj)

        return dirs
