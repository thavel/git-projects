from future.utils import with_metaclass
from uuid import uuid4


# Abstract classes

class ShortcutHolder(type):
    REGISTRY = dict()

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        if new_cls.option:
            mcs.REGISTRY[new_cls.option] = new_cls
        return new_cls


class Shortcut(with_metaclass(ShortcutHolder, object)):
    option = None
    description = None
    output = True

    def __init__(self):
        pass

    @staticmethod
    def commands():
        raise NotImplementedError()


# Shortcut implementations

class Current(Shortcut):
    option = 'current'
    description = 'display current branch name'

    @staticmethod
    def commands():
        yield 'rev-parse', '--abbrev-ref', 'HEAD'


class Update(Shortcut):
    option = 'update'
    description = 'update and rebase the current local branch with origin'

    @staticmethod
    def commands():
        yield 'fetch', 'origin', '--prune'
        yield 'pull', '--rebase'


class Reset(Shortcut):
    option = 'reset'
    output = False
    description = 'discard any local changes and switch to an up-to-date ' \
                  'version of the master branch'

    @staticmethod
    def commands():
        tmp = 'tmp' + str(uuid4())[:8]
        yield 'reset', '--hard'
        yield 'checkout', '-b', tmp
        yield 'branch', '-D', 'master'
        yield 'fetch', 'origin', '--prune'
        yield 'checkout', 'master'
        yield 'branch', '-D', tmp
