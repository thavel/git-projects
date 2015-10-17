# git-projects

[![Circle CI](https://img.shields.io/circleci/project/thavel/git-projects/master.svg)](https://circleci.com/gh/thavel/git-projects) [![pypi version](http://img.shields.io/pypi/v/git-projects.svg)](https://pypi.python.org/pypi/git-projects) [![pypi download week](http://img.shields.io/pypi/dw/git-projects.svg)](https://pypi.python.org/pypi/git-projects)


Pure git commands for multi-repository projects.

## Requirements

* [Git](http://git-scm.com)
* [Python](https://www.python.org) (2 or 3)

## Getting started

Install dependencies

```bash
apt-get install git python # alternatively use brew on OSX
pip install git-projects
```

Create your `.gitprojects` file in your `$HOME` directory.

## Command line syntax

```bash
gp <projects> <git command>
```

Projects are pointed out using `@`. You shall not use `git` in your commands. For instance, to perform `git fetch origin --prune` in each repository of your project `my-project`:

```bash
gp @my-project fetch origin --prune
```

You can also provide several projects as targets of your git command:

```bash
gp @project1 @project2 pull --rebase
```

## Configuration syntax

### Basic project

Here is a basic example of a project.

```yaml
my-project:
    path: ~/workspace/my-project
    repositories:
        - my-lib1
        - my-lib2
        - my-service1
        - my-service2
```

In this case, `repositories` is optional, then all directories in `path` will be used as targets of your git command.

### Multi-path project

You can also defined `repositories` using paths. In this case, you shall no set a `path`.

```yaml
multipath-project:
    repositories:
        - ~/workspace/my-project/
        - ~/my-compagny/a-project/a-lib/
        - ~/data/my-external-hd/my-lyb/
```

### Sub-projects

You can defined `subprojects`, so that if you target a specific project, all sub-projects are targeted.

```yaml
main-project:
    path: ~/workspace/my-service/
    repositories:
        - my-lib1
        - my-lib2
    subprojects:
        - second-project
        
second-project:
    path: ~/workspace/my-lib/
    repositories:
        - my-module1
        - my-module2
```
