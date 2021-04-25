from fabric.api import env, run
from fabric.operations import sudo

GITHUB_REPO = "https://github.com/zmrenwu/django-blog-zm.git"

env.user = 'yangxg'
env.passwords = {'yangxg@zmrenwu.com:26801': '940330'}
env.hosts = ['zmrenwu.com']
env.port = '26801'
env.password = '940330'


def deploy():
    source_folder = '/home/yangxg/sites/zmrenwu.com/django-blog-zm'
    env_folder = '/home/yangxg/sites/zmrenwu.com/env/bin/'
    secret_key = 'c#hs(4(57939)x0tt)v)nz@%8-^x01$d=_)t*2=@=t#3ot$5&r'

    sudo('stop gunicorn-zmrenwu.com')
    run('cd %s && git pull' % source_folder)
    run("""
        export DJANGO_SECRET_KEY='{}' &&
        export DJANGO_SETTINGS_MODULE='config.settings.production' &&
        cd {} &&
        ../env/bin/python3 manage.py collectstatic --noinput
        """.format(secret_key, source_folder))
    # run("export DJANGO_SETTINGS_MODULE='config.settings.production'")
    # run('cd %s && ../env/bin/python3 manage.py collectstatic --noinput' % source_folder)
    sudo('start gunicorn-zmrenwu.com')
    sudo('service nginx reload')
