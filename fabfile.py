from fabric.api import *
env.use_ssh_config = True
env.hosts = ['dsl']
def deploy():
    code_dir = '~/program/nodejs/blog'
    with cd(code_dir):
        run("git pull")
         #deploy static site
        run("hexo clean")
        run("hexo g")
        run("cp -r public/* ~/program/html/blog/note")
