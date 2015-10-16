import yaml
from os.path import expanduser


class ConfigError(Exception):
    pass


class ConfigParser(object):

    def __init__(self, file_path):
        self.file_path = expanduser(file_path)
        self.config = self.parse(self.file_path)

    @staticmethod
    def parse(file_path):
        with open(file_path, 'r') as file_content:
            return yaml.load(file_content)

    @property
    def projects(self):
        """
        Gives the list of projects
        """
        return self.config.keys()

    def path(self, project):
        path = self.config[project].get('path', None)

        if not path:
            return
        return expanduser(path)
