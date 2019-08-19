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
    'deploy',
    'plantgl',
    'plantscan3d',
    ('libqglviewer-recipe' , 'OpenAleaRecipes'),
    'pyqglviewer'
]

owner = sys.argv[1] if len(sys.argv) >= 2 else 'openalea'
branch = sys.argv[2] if len(sys.argv) >= 3 else 'master'

# ------
# Script
# ------

def removeFromConfig(name, configfile = '.gitmodules'):
    moduleinfo = open(configfile).read()
    modules = moduleinfo.split('[submodule ')
    modules = [m for m in modules if not m.startswith('"'+name+'"')]
    newmoduleinfo = '[submodule '.join(modules)
    open(configfile+'-bckup','w').write(moduleinfo)
    open(configfile,'w').write(newmoduleinfo)

def config(name, configfile = '.gitmodules'):
    moduleinfo = open(configfile).read()
    modules = moduleinfo.split('[submodule ')
    for m in modules :
        if m.startswith('"'+name+'"'):
            lines = m.splitlines()[1:]
            cfg= {}
            for l in lines:
                k,v = l.split('=')
                cfg[k.strip()] =v.strip()
            return cfg


def execProgram(program, *args):
    args = [program] + list(args)
    print (' '.join(args))
    child = subprocess.run(args, stdout=subprocess.PIPE)
    #child.communicate()
    return child.returncode, child.stdout.decode()

def execGit(*args):
    return execProgram('git', *args)


eNotExists, eRemoteExists, eBranchExists = 0,1,2

class Repository:

    def __init__(self, owner, name, branch='master', defaultowner = 'openalea', defaultbranch = 'master'):
        self.name = name
        self.owner = owner
        self.branch = branch
        self.defaultowner = defaultowner
        self.defaultbranch = defaultbranch

    def check(self):
        code = self.checkRemoteRepoExists()
        if code & eRemoteExists == 0:
            print('Cannot find asked remote owner of'+repr(self.name)+'. Changing from',repr(self.owner),"to '"+self.defaultowner+"'")
            self.owner = self.defaultowner
        if code & eBranchExists == 0:
            print('Cannot find asked remote branch of'+repr(self.name)+'. Changing from',repr(self.branch),"to '"+self.defaultbranch+"'")
            self.branch = self.defaultbranch

    def checkRemoteRepoExists(self):
        code, value = execGit('ls-remote', 'https://github.com/' + self.owner + '/' + self.name + '.git', '-b', self.branch)
        if code != 0 : return eNotExists
        elif self.branch in value : return eBranchExists | eRemoteExists
        else : return eRemoteExists

    def update(self):
        if os.path.exists(self.name) :
            print('Submodule',self.name,'already exists. Updating')
        if not os.path.exists(self.name) :
            self.cloneAsSubmodule()
        else :
            lowner = self.localRepoOwner()
            lbranch = self.localRepoBranch()
            print('Current owner:',repr(lowner),'- current branch:',repr(lbranch))
            if lowner != self.owner :
                self.removePreviousSubmodule()
                self.cloneAsSubmodule()
                os.chdir(self.name)
                execGit('checkout',self.branch)
                os.chdir(os.pardir)
            elif lbranch != self.branch:
                os.chdir(self.name)
                execGit('checkout',self.branch)
                execGit('pull')
                os.chdir(os.pardir)
            else:
                os.chdir(self.name)
                execGit('pull')
                os.chdir(os.pardir)


    def cloneAsSubmodule(self):
        return execGit('submodule', 'add', 'https://github.com/' + self.owner + '/' + self.name + '.git', self.name, '-b', self.branch)

    def removePreviousSubmodule(self):
        if os.path.exists(self.name):
            removeFromConfig(self.name)
            execGit('add', '.gitmodules')
            execGit('submodule', 'deinit', self.name)
            execGit('rm', '--cached', self.name)
            execProgram('rm','-rf',join('.git','modules',self.name))
            execGit('commit', '-m', '"Remove submodule '+self.name+'"')
            execProgram('rm','-rf',self.name)

    def localRepoOwner(self):
        # does not work. cannot grap remote repo
        remotesignature = 'https://github.com/'
        if os.path.exists(self.name):
            value = config(self.name)['url']
            if value.startswith(remotesignature):
                currentowner = value[len(remotesignature):].split('/')[0]
                return currentowner

    def localRepoBranch(self):
        # does not work. cannot grap remote branch
        if os.path.exists(self.name):
            os.chdir(self.name)
            code, value = execGit('branch')
            os.chdir(os.pardir)
            for l in value.splitlines():
                if l.startswith('*'):
                    return l.split()[1]



if __name__ == '__main__':
    # Clone submodule
    for repoName in repositories:
        defaultparam = []
        if type(repoName) != str:
            defaultowner = repoName[1:]
            repoName = repoName[0]
        print('*** Processing submodule '+repr(repoName))
        repo = Repository(owner, repoName, branch, *defaultparam)
        repo.check()
        repo.update()

