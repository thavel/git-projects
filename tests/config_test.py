from unittest import TestCase

from yaml import load
from git_projects.config import ConfigParser, ConfigError


SAMPLE = """
my-project:
  path: ~/workspace/test/
  repositories:
    - lib1
    - lib2
"""


class ConfigParserMock(ConfigParser):

    @staticmethod
    def parse(file_path):
        return load(SAMPLE)


class TestConfig(TestCase):

    def setUp(self):
        self.parser = ConfigParserMock('file.yml')

    def test_001_validation(self):
        self.assertRaises(ConfigError, self.parser.validation, 'test')
