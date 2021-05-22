#!/usr/bin/env python3
import pathlib
import re
import sys

from setuptools import find_packages, setup


BASE_DIR = pathlib.Path(__file__).parent
README_PATH = BASE_DIR / 'README.rst'
PACKAGE_PATH = BASE_DIR / 'freedictionaryapi'
PACKAGE_INIT_PATH = PACKAGE_PATH / '__init__.py'


MINIMAL_PYTHON_VERSION = (3, 6)
if sys.version_info < MINIMAL_PYTHON_VERSION:
    raise RuntimeError(
        'freedictionaryapi works only with Python {}+'.format(
            '.'.join(map(str, MINIMAL_PYTHON_VERSION))
        )
    )


def get_version() -> str:
    """
    Get version of the `freedictionaryapi` package.

    :return: version of the `freedictionaryapi` package
    :rtype: str
    """

    with open(PACKAGE_INIT_PATH, 'r', encoding='utf-8') as file:
        init_file_content = file.read()

    try:
        return re.findall(r"^__version__ = '([^']+)'\r?$", init_file_content, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


def get_long_description() -> str:
    """
    Get full description from `README.rst`.

    :return: full description from `README.rst`
    :rtype: str
    """

    with open(README_PATH, 'r', encoding='utf-8') as file:
        long_description = file.read()

    return long_description


setup(
    name='python-freeDictionaryAPI',
    version=get_version(),
    packages=find_packages(exclude=('tests', 'examples', 'docs', 'Pipfile', 'Pipfile.lock')),
    url='https://github.com/Max-Zhenzhera/python-freeDictionaryAPI',
    license='MIT',
    author='Max Zhenzhera',
    requires_python='>=3.6',
    author_email='maxzhenzhera@gmail.com',
    description='Wrapper for Free Dictionary API https://dictionaryapi.dev/',
    long_description=get_long_description(),
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=[
    ],
    extras_require={
        'async-client': [
            'aiohttp>=3.7.4.post0',
        ],
        'sync-client': [
            'httpx>=0.18.1',
        ],
    },
    project_urls={
        'Documentation': 'https://python-freedictionaryapi.readthedocs.io/',
        'Source': 'https://github.com/Max-Zhenzhera/python-freeDictionaryAPI',
        'Bug Tracker': 'https://github.com/Max-Zhenzhera/python-freeDictionaryAPI/issues',
    },
)
