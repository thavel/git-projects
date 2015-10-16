from git_projects.config import ConfigParser, ConfigError


GPROJECTS = '~/.gprojects'


def main():
    parser = ConfigParser(GPROJECTS)
    print(parser.projects)
    print(parser.path('surycat-v4'))


if __name__ == "__main__":
    main()

