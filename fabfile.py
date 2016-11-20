from fabric.api import *
env.hosts = ['43.242.128.158']
env.user = 'dengsl'
def deploy():
    code_dir = '/home/dengsl/program/nodejs/blog'
    with cd(code_dir):
        run("git pull")
         #deploy static site
        run("hexo clean")
        run("hexo g")
        run("cp -r public/* /home/dengsl/program/html/blog/note")
