# -*- encoding: utf-8 -*-

import os
import stat
import shutil
import subprocess

from cookiecutter.main import cookiecutter


TARGET_DIR = '.release'
APP_CONFIG_DIR = '.app'
API_EXPORT = 'apis.py'


def _rm_pre_release(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(path)


def _build():
    subprocess.run(
        ["pipenv", "run", "python", "setup.py", "build"],
        check=True,
        universal_newlines=True
    )


def _install_deppackages_ifneed():
    with open("Pipfile", 'r') as file:
        packages = file.read()

    if packages.find('connexion') > 0 and packages.find('tornado') > 0:
        return

    subprocess.run(
        ["pipenv", "install", "connexion[swagger-ui]", "tornado"],
        check=True,
        universal_newlines=True
    )


DOCKER_FILE_CONTENT = """
FROM python:3.7.2-alpine3.9

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 9502
CMD python ./app.py
"""


def _generate_docker_file():
    with open(os.path.join(TARGET_DIR, "Dockerfile"), 'w') as fp:
        fp.write(DOCKER_FILE_CONTENT)


def release_as_REST(app_settings, with_docker_file=False, **kwargs):
    if os.path.exists(TARGET_DIR):
        _rm_pre_release(TARGET_DIR)

    cookiecutter(
        kwargs['tmpl_dir'],
        no_input=True,
        overwrite_if_exists=True,
        extra_context={
            "app": app_settings.json()
        }
    )

    if not os.path.exists(APP_CONFIG_DIR):
        shutil.copytree(
            os.path.join(TARGET_DIR, APP_CONFIG_DIR),
            APP_CONFIG_DIR
        )
        shutil.copyfile(
            os.path.join(TARGET_DIR, API_EXPORT),
            os.path.join("src", app_settings.app_name, API_EXPORT)
        )
    else:
        shutil.rmtree(
            os.path.join(TARGET_DIR, APP_CONFIG_DIR)
        )
        shutil.copytree(
            APP_CONFIG_DIR,
            os.path.join(TARGET_DIR, APP_CONFIG_DIR)
        )
    os.remove(os.path.join(TARGET_DIR, API_EXPORT))

    _install_deppackages_ifneed()
    _build()

    shutil.copytree(
        os.path.join("build", "lib", app_settings.app_name),
        os.path.join(TARGET_DIR, "lib", app_settings.app_name)
    )

    with open(os.path.join(TARGET_DIR, "requirements.txt"), 'w') as fp:
        subprocess.run(
            ["pipenv", "lock", "-r"],
            check=True,
            universal_newlines=True,
            stdout=fp
        )

    if with_docker_file:
        _generate_docker_file()

    return """
start your app: cd .release & pipenv run python app.py

Visit your app by url: http://localhost:9502/ui
"""


def release_to_pypi():
    return subprocess.run(
        ["make", "release"],
        check=True,
        universal_newlines=True
    )


def release_app(app_settings, with_docker_file=False, **kwargs):
    """
    发布APP

    该方法会根据项目中的.pycake中的相关配置进行发布操作

    该发布操作目前只支持发布为基于swagger的REST服务

    """

    if app_settings.get('openapi_enabled', False):
        return release_as_REST(
            app_settings,
            with_docker_file=with_docker_file,
            **kwargs
        )
    else:
        return release_to_pypi()
