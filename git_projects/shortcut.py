from uuid import uuid4


def current():
    yield 'rev-parse', '--abbrev-ref', 'HEAD'


def update():
    yield 'fetch', 'origin', '--prune'
    yield 'reset', '--hard'
    yield 'pull', '--rebase'


def reset(branch):
    tmp_branch = uuid4()[:8]
    yield 'reset', '--hard'
    yield 'checkout', '-b', tmp_branch
    yield 'branch', '-D', branch
    yield 'checkout', branch
    yield 'branch', '-D', tmp_branch


def master():
    return reset('master')


SHORTCUTS = [current, update, reset, master]
