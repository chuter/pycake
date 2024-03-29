# -*- encoding: utf-8 -*-

import os
import stat
import shutil
import subprocess

from cookiecutter.main import cookiecutter


TARGET_DIR = '.release'
APP_CONFIG_DIR = '.app'
API_EXPORT = 'apis.py'
TCLOUD_DIR = '.tcloud'
MODEL_DIR = os.path.join('lib', 'model')
MIDDLEWARN_FILE = os.path.join(MODEL_DIR, 'middleware.py')

INSTALL_PACKAGE_COMMON_ARGS = ["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"]


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


def _install_deppackages_ifneed(app_settings):
    with open("Pipfile", 'r') as file:
        packages = file.read()

    if app_settings.openapi_model:
        if packages.find('sanic') > 0 and packages.find('aiologger') > 0:
            return

        if app_settings.model_sample:
            subprocess.run(
                ["pipenv", "install", "aiologger", "sanic", "sanic_openapi",
                 "\"aiofiles>=0.6.0\""] + INSTALL_PACKAGE_COMMON_ARGS,
                check=True,
                universal_newlines=True
            )
        else:
            subprocess.run(
                ["pipenv", "install", "sanic", "sanic_openapi"] + INSTALL_PACKAGE_COMMON_ARGS,
                check=True,
                universal_newlines=True
            )
    else:
        if packages.find('connexion') > 0 and packages.find('aiohttp') > 0:
            return

        subprocess.run(
            ["pipenv", "install", "connexion[swagger-ui]", "tornado", "aiohttp",
             "aiohttp-jinja2"] + INSTALL_PACKAGE_COMMON_ARGS,
            check=True,
            universal_newlines=True
        )


DOCKER_FILE_CONTENT = """
FROM harbor.weizhipin.com/tcloud/python:xgboost-02

COPY .release/ /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 9502
CMD python ./app.py
"""


DATASCIENCE_PACKAGES = ['numpy', 'pandas', 'matplotlib', 'scipy', 'scikit-learn', 'nltk', 'xgboost']


# TODO(chuter): 细化对Image的检测和对requirements的修改
def _generate_docker_file(**kwargs):
    print('>> generation docker file')
    is_based_datascience = False
    with open(os.path.join(TARGET_DIR, "requirements.txt"), 'r') as f:
        requires = f.read()
        if (requires.find('numpy') > 0 or requires.find('pandas') > 0):
            is_based_datascience = True

    if is_based_datascience:
        # remove packages included in image yet
        with open(os.path.join(TARGET_DIR, "requirements.txt_"), 'w') as fout:
            with open(os.path.join(TARGET_DIR, "requirements.txt"), 'r') as fin:
                for line in fin.readlines():
                    should_skip_line = False
                    for package in DATASCIENCE_PACKAGES:
                        if (line.find(package) >= 0):
                            should_skip_line = True
                            break

                    if not should_skip_line:
                        fout.write(line)

        os.remove(os.path.join(TARGET_DIR, "requirements.txt"))
        os.rename(
            os.path.join(TARGET_DIR, "requirements.txt_"),
            os.path.join(TARGET_DIR, "requirements.txt")
        )

    if not os.path.isfile(os.path.join(TCLOUD_DIR, "Dockerfile")):
        with open(os.path.join(TCLOUD_DIR, "Dockerfile"), 'w') as fp:
            fp.write(DOCKER_FILE_CONTENT)


def release_as_REST(app_settings, with_docker_file=False, **kwargs):
    if os.path.exists(TARGET_DIR):
        print('>> removing old release')
        _rm_pre_release(TARGET_DIR)

    print('>> building...')
    app = app_settings.json()
    app.update(os.environ.__dict__)
    cookiecutter(
        kwargs['tmpl_dir'],
        no_input=True,
        overwrite_if_exists=True,
        extra_context={
            "app": app
        }
    )

    if not app_settings.openapi_model:
        if not os.path.exists(APP_CONFIG_DIR):
            shutil.copytree(
                os.path.join(TARGET_DIR, APP_CONFIG_DIR),
                APP_CONFIG_DIR
            )
        else:
            shutil.rmtree(
                os.path.join(TARGET_DIR, APP_CONFIG_DIR)
            )
            shutil.copytree(
                APP_CONFIG_DIR,
                os.path.join(TARGET_DIR, APP_CONFIG_DIR)
            )
    else:
        shutil.rmtree(
            os.path.join(TARGET_DIR, APP_CONFIG_DIR)
        )

    if not os.path.exists(os.path.join("src", app_settings.app_name, API_EXPORT)):
        shutil.copyfile(
            os.path.join(TARGET_DIR, API_EXPORT),
            os.path.join("src", app_settings.app_name, API_EXPORT)
        )

    if not os.path.exists(TCLOUD_DIR):
        shutil.copytree(
            os.path.join(TARGET_DIR, TCLOUD_DIR),
            TCLOUD_DIR
        )

    if not app_settings.openapi_model:
        shutil.rmtree(
            os.path.join(TARGET_DIR, MODEL_DIR)
        )
    else:
        if not app_settings.model_sample:
            os.remove(os.path.join(TARGET_DIR, MIDDLEWARN_FILE))
        else:
            os.makedirs(os.path.join(TARGET_DIR, "sample"), exist_ok=True)

    os.remove(os.path.join(TARGET_DIR, API_EXPORT))

    _install_deppackages_ifneed(app_settings)
    _build()

    shutil.copytree(
        os.path.join("build", "lib", app_settings.app_name),
        os.path.join(TARGET_DIR, "lib", app_settings.app_name),
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc')
    )

    with open(os.path.join(TARGET_DIR, "requirements.txt"), 'w') as fp:
        subprocess.run(
            ["pipenv", "lock", "-r"],
            check=True,
            universal_newlines=True,
            stdout=fp
        )

    if with_docker_file:
        _generate_docker_file(**kwargs)

    if app_settings.openapi_model:
        return """
start your app: cd .release & pipenv run python app.py

Visit your app by url: http://localhost:9502/swagger
"""
    else:
        return """
start your app: cd .release & pipenv run python app.py

Visit your app by url: http://localhost:9502/api/ui
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
