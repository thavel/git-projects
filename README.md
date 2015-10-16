# git-projects

Pure git commands for multi-repository projects.

## Requirements

* Git
* Python 3
* [libgit2](https://libgit2.github.com)
* [cffi](https://pypi.python.org/pypi/cffi/1.2.1)

## Getting started

Install dependencies

```bash
apt-get install git python3 libgit2  # alternatively use brew on OSX
pip install cffi git-projects
```

Create your `.gprojects` file in your `$HOME` directory.

## Command line syntax

```bash
gp <projects> <git command>
```

For instance, to perform `git fetch origin --prune` in each repository of your project `my-project`:

```bash
gp @my-project fetch origin --prune
```

You can also provide several projects as targets of your git command:

```bash
gp @project1 @project2 pull --rebase
```

## Configuration syntax

### Basic project

```yaml
my-project:
    path: ~/workspace/my-project
    repositories:
        - my-lib1
        - my-lib2
        - my-service1
        - my-service2
```

### Multi-path project

```yaml
multipath-project:
    repositories:
        - ~/workspace/my-project/
        - ~/my-compagny/a-project/a-lib/
        - ~/data/my-external-hd/my-lyb/
```

### Sub-projects

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