#!/usr/bin/env python3
import os
try:
    from git import Repo
except ImportError:
    import pip
    pip.main(['install', '--user', "GitPython"])
    from git import Repo

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def main():
    if ('No license file' == '{{ cookiecutter.open_source_license }}'):
        remove_file('LICENSE')

    repo = Repo.init('.')
    git = repo.git
    if ('yes' == '{{ cookiecutter.add_lib_submodule }}'):
        git.submodule('add', 'https://github.com/kylebarron/lib')
        os.system('git submodule update --init --recursive')
        # repo.submodule_update(init=True, recursive=True)

def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':
    main()
