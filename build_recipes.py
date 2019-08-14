import os, shutil
from os.path import join
import subprocess
import sys

# -------------
# Configuration
# -------------

repositories = [
    'lpy',
    'mtg',
    'openalea.deploy',
    'plantgl',
    'plantscan3d',
    'libqglviewer-recipe',
    'pyqglviewer'
]

owner = sys.argv[1]
branch = sys.argv[2] if len(sys.argv) >= 3 else 'master'

# ------
# Script
# ------

class Repository:

    def __init__(self, owner, name, branch='master'):
        self.owner = owner
        self.name = name
        self.branch = branch

    def cloneAsSubmodule(self):
        return self.__execGit('submodule', 'add', 'https://github.com/' + self.owner + '/' + self.name + '.git', self.name, '-b', self.branch)

    def removePreviousSubmodule(self):
        if os.path.exists(self.name):
            #self.__execGit('submodule', 'deinit', '-f', self.name)
            #try:
            #    shutil.rmtree(join('.git', 'modules', self.name))
            #except:
            #    pass
            self.__execGit('rm', '-f', self.name)


    def __execGit(self, *args):
        return self.__execProgram('git', *args)

    def __execProgram(self, program, *args):
        args = [program] + list(args)
        child = subprocess.Popen(args)
        child.communicate()
        return child.returncode

# Clone submodule
for repoName in repositories:
    repo = Repository(owner, repoName, branch)
    repo.removePreviousSubmodule()
    repo.cloneAsSubmodule()
