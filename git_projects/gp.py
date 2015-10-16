from git_projects.config import ConfigParser
from yaml.error import YAMLError


GPROJECTS = '~/.gprojects'


def main():
    # YAMLError, FileNotFoundError
    parser = ConfigParser(GPROJECTS)
    print(parser.directories('my-project'))


if __name__ == "__main__":
    main()
