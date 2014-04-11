from contextlib import contextmanager as _contextmanager
from fabric.api import cd, env, local, run, sudo, task, put, hide
from fabric.context_managers import prefix, settings
from fabric.contrib.files import append
from fabric.operations import prompt
import os, re, tempfile, time
import subprocess, json

#from helpers.models_to_forms import jsmodels

env.use_ssh_config = True # ~/.ssh/config
env.use_sudo = True

env.local_project_root = os.path.dirname(__file__)
env.local_python_packages_dir = os.path.join(env.local_project_root, 'dist')
# SETTINGS
env.project = 'facegame'
env.deploy_group = 'Users' # deploy users must belong to this group
env.www_root = '/srv/www'
env.user = os.environ['USER']
env.owner = 'www-data'
env.release = '%s_%s' % (env.project, time.strftime('%Y%m%d%H%M%S'))
env.pkg = '/tmp/{release}.tar.gz'.format(**env)
env.apache_restart_command = 'service apache2 restart'
env.basepath = '{www_root}/{project}'.format(**env)
env.project_root = '{www_root}/{project}/www'.format(**env)
env.python_packages_dir = '{www_root}/{project}/dist'.format(**env)
env.virtualenv = '{www_root}/{project}/venv'.format(**env)
env.supervisor_conf_dir = '/etc/supervisor'
env.branch = 'fum5'

#
#
# TASKS
#
#

# supervisor_conf()
# supervisor_restart()

@task
def deploy():
    ask_sudo_password()

    dirs()

    tar_from_git()
    upload_tar()

    prepare_python_packages()
    synchronize_python_packages()
    install_python_packages()
    
    # anything that depends on requirements under here
    # jsurls need to be re-generated with production settings
    #jsmodels(apps=['common','contenttypes'], filename='static/js/gen/custom_form_tpl.js',)
    prepare_node_packages()
    prepare_assets()

    #manage('migrate --noinput')
    manage('syncdb --noinput')

    # prepare_hidden_files()
    ownership()

    restart_apache()

@task
def ownership():
    sudo('chown -fR {owner} {basepath}/media'.format(**env))
    sudo('chown -fR {owner} {basepath}'.format(**env))
    with settings(hide('warnings',), warn_only=True):
        sudo('chown -fR {owner} {basepath}/sqlite.db'.format(**env))

@task
def dirs():
    sudo('mkdir -p {basepath} {basepath}/packages {basepath}/releases {basepath}/media {basepath}/dist {basepath}/static'.format(**env))

    # backups
    sudo('mkdir -p /srv/backup/postgres'.format(**env))
    sudo('chown -fR {owner} /srv/backup/postgres'.format(**env))

@task
def setup():
    ask_sudo_password()

    dirs()
    ownership()
    tar_from_git()
    upload_tar()

    prepare_python_packages()
    synchronize_python_packages()
    create_virtualenv()
    install_python_packages()

    prepare_node_packages()
    prepare_assets()
    # prepare_hidden_files()

    restart_apache()

# @task
# def prepare_hidden_files():
#     sudo('cp /root/local_settings.py {project_root}/'.format(**env))

# @task
# def check():
#     """ check project is setup correctly
#     DJANGO_SETTINGS_MODULE exported in venv/bin/activate
#     """
#     result = sudoin('env|grep DJANGO_SETTINGS_MODULE')
#     assert 'settings.prod' in result

@task
def reset_and_sync():
    manage('reset_db --router=default --noinput')
    manage('syncdb --noinput')
    manage('datamigrate')

#
#
# UNDER THE HOOD
#
#

@task
def prepare_assets():
    with virtualenv():
        with cd(env.project_root):
            sudo('assetgen --profile dev assetgen.yaml --force')
    manage('collectstatic --noinput')

@task
def restart_apache():
    cmd = getattr(env, 'apache_restart_command', '/etc/init.d/apache2 restart')
    sudo(cmd, pty=False)

def filenameToRequirement(filename):
    """Converts 'package-name-1.2.3.tar.gz' to 'package-name==1.2.3'"""
    match = re.match(r'(.+)-(\d.+?)(\.tar\.gz|\.tar\.bz2|\.zip)$', filename)
    if not match:
        return None
    package, version, _extension = match.groups()
    return '{package}=={version}'.format(package=package, version=version)

@task
def prepare_python_packages():
    local('mkdir -p {local_python_packages_dir}'.format(**env))
    local('cp'
          ' {local_project_root}/requirements.txt'
          ' {local_python_packages_dir}/'
          .format(**env))
    existing_files = set(
        filenameToRequirement(filename)
        for filename in os.listdir(env.local_python_packages_dir))
    missing_requirements = tempfile.NamedTemporaryFile()
    for raw_line in open(os.path.join(env.local_project_root, 'requirements.txt')):
        line = raw_line.strip()
        if not line or line.startswith('#') or line not in existing_files:
            missing_requirements.write(raw_line)
    missing_requirements.flush()
    local('pip install'
          ' -d {env.local_python_packages_dir}'
          ' --exists-action=i'
          ' -r {missing_requirements_file}'
          .format(env=env, missing_requirements_file=missing_requirements.name))
    missing_requirements.close()
    local_venv = '{local_python_packages_dir}/virtualenv.py'.format(**env)
    if hasattr(env, 'virtualenv') and not os.path.isfile(local_venv):
        local('wget -O {local_python_packages_dir}/virtualenv.py'
              ' https://raw.github.com/pypa/virtualenv/master/virtualenv.py'
              .format(**env))

def rsync_up(args, source, target):
    sudo('mkdir -p {target}'.format(env=env, target=target))
    sudo('chgrp {env.deploy_group} {target} && chmod -R g+w {target}'.format(env=env, target=target))
    if env.key_filename:
        args += " -e 'ssh -i %s'" % env.key_filename[0]
    local('rsync -r {args} {source}/ {env.user}@{env.host}:{target}'.format(env=env, args=args, source=source, target=target))


@task
def synchronize_python_packages():
    rsync_up('-vP'
             ' --delete'
             ' --delete-excluded'
             ' --include=*.tgz'
             ' --include=*.tar.gz'
             ' --include=*.zip'
             ' --include=virtualenv.py'
             ' --include=requirements.txt'
             ' --exclude=*',
             source=env.local_python_packages_dir,
             target=env.python_packages_dir)

@task
def create_virtualenv():
    sudo('pip install virtualenv --upgrade')
    if hasattr(env, 'virtualenv'):
        sudo('rm -rf {virtualenv} && '
             'virtualenv'
             ' --extra-search-dir={python_packages_dir}'
             ' --prompt="({project})"'
             ' {virtualenv}'
             .format(**env))
    

@_contextmanager
def virtualenv():
    if hasattr(env, 'virtualenv'):
        with prefix('source {virtualenv}/bin/activate'.format(**env)):
            yield
    else:
        yield

@task
def install_python_packages():
    with virtualenv():
        sudo("cat {python_packages_dir}/requirements.txt|grep -v '^--' > {python_packages_dir}/files.txt".format(**env))
        pip_install('-r <(grep -vxFf'
                    '     <(pip freeze)'
                    '     {python_packages_dir}/files.txt)'
                    .format(**env))

@task
def ask_sudo_password():
    sudo('echo Enter sudo password for {env.host}'.format(env=env))

def umask(value='002'):
    return prefix('umask {value}'.format(value=value))

def pip_install(packages):
    sudo('HOME={env.project_root} pip install'
         ' --default-timeout=5'
         ' --no-index'
         ' -f file://{env.python_packages_dir}'
         ' {packages}'
         .format(env=env, packages=packages))
    

@task
def manage(args):
    with virtualenv():
        with cd(env.project_root):
            return sudo('DJANGO_SETTINGS_MODULE=facegame.settings.prod python manage.py {args}'.format(args=args))

@task
def sudoin(cmd):
    with virtualenv():
        with cd(env.project_root):
            return sudo(cmd)

def aptgetall():
    all = """
    apt-get install --ignore-missing \
    build-essential curl \
    git git-core 
    """
    # supervisor \
    # libxml2-dev libxslt1-dev \
    # libcurl4-openssl-dev libssl-dev zlib1g-dev checkinstall libpcre3-dev \
    # libsqlite3-dev libbz2-dev \
    # nodejs npm
    # """


#
# ALIASES
#
#

def mput(a, b, **kwargs):
    if env.use_sudo:
        kwargs['use_sudo'] = True
    return put(a.format(**env), b.format(**env), **kwargs)

def mrun(a, **kwargs):
    if env.use_sudo:
        return sudo(a.format(**env), **kwargs)
    else:
        return run(a.format(**env), **kwargs)

def mlocal(a, **kwargs):
    return local(a.format(**env), **kwargs)

#
# FILE HANDLING
#
#
    
def upload_tar():
    mput(env.pkg, '{basepath}/packages/')
    with cd(env.basepath):
        mrun('mkdir -p releases/{release}')
        mrun('tar zxf packages/{release}.tar.gz -C releases/{release}')
    symlink_release()
    mlocal('rm {pkg}')

def tar_from_git():
    local('git archive --format=tar {branch} | gzip > {pkg}'.format(**env))

def symlink_release():
    with cd(env.basepath):
        mrun('ln -s releases/{release} www.new; mv -T www.new www')

@task
def prepare_node_packages():
    with virtualenv():
        sudo('pip install nodeenv --upgrade')
        with cd(env.basepath):
            sudo('[ -f "venv/bin/node" ] || nodeenv -p --node=0.10.26')

    with virtualenv():
        with cd(env.project_root):
            sudo('cp package.json {basepath}'.format(**env))
            sudo('ln -sf {basepath}/node_modules/ .'.format(**env))
        with cd(env.basepath):
            sudo('npm install')

    # TODO: read package.json? glob binaries instead of implicit?
    binaries = [('less','lessc'),]
    for pkg,binary in binaries:
        with cd('{basepath}/venv/bin'.format(**env)):
            sudo('ln -sf {basepath}/node_modules/{pkg}/bin/{binary} .'.format(
                basepath=env.basepath,
                pkg=pkg,
                binary=binary,))

#
# SUPERVISOR (server-wide setup with individual project settings)
#
#

# def supervisor_conf():
#     mput('{project}.conf'.format(env), '{supervisor_conf_dir}/conf.d/')
    
# def start_app():
#     with settings(hide('warnings',), warn_only=True):
#         res = mrun("supervisorctl start all")
#         if not res.succeeded or 'no such file' in res:
#             run("supervisord")

# def stop_app():
#     with settings(hide('warnings',), warn_only=True):
#         run("supervisorctl stop all")
#         run("supervisorctl shutdown")

# def supervisor_restart():
#     with settings(hide('warnings',), warn_only=True):
#         stop_app()
#         start_app()

# def supervisor_soft_restart_app():
#     with settings(hide('warnings',), warn_only=True):
#         run("supervisorctl restart all")


