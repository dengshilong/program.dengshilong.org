from fabric.api import *
env.hosts = ['188.166.217.140']
env.user = 'dengsl'
def deploy():
    code_dir = '/home/dengsl/program/nodejs/blog'
    with cd(code_dir):
        run("git pull")
