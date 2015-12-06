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

You can also create a `gitprojects.yml` or `.gitprojects` file in any folder you want for a local use.

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

## Command shortcuts

This tool also provides shortcuts for lazy users. Basically, instead of using pure git commands, you're allowed to do:

```bash
gp @my-project --<shortcut>
```

For instance, if you want to `fetch`, discard any local changes and `pull` the `origin/master` branch, you can simply do:

```bash
gp @my-project --reset
```

The following table gives you the list of implemented shortcuts (also available through `--help`).

| Shortcut    | Description                                                                        |
|-------------|------------------------------------------------------------------------------------|
| `--current` | display current branch name                                                        |
| `--update`  | update and rebase the current local branch with origin                             |
| `--reset`   | discard any local changes and switch to an up-to-date version of the master branch |


## Configuration syntax

### Basic project

Here is a basic example of a project.

```yaml
my-project:
    origin: git@github.com:thavel
    path: ~/workspace/my-project
    repositories:
        - my-lib1
        - my-lib2
        - my-service1
        - my-service2
```

In this case, `repositories` is optional, then all directories in `path` will be used as targets of your git command.

The `origin` is also optional. It is used to enable the cloning feature: if a repository does not exist at the specified path, this tool will try to clone it.
Sub-projects inherit this parameter. So, basically, if your `.gitprojects` file is properly set, you can bootstrap the repositories of your whole project(s) with a single command (`gp @my-project fetch`, for instance).

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

## Upcoming features

* Asynchronous tasks
* Project names completion
* Git commands completion
