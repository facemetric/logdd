import inspect
import os

import setuptools

__location__ = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))


def __read_version(package):
    with open(os.path.join(package, '__init__.py'), 'r') as fd:
        for line in fd:
            if line.startswith('__version__ = '):
                return line.split()[-1].strip().strip("'")


NAME = 'logdd'
MAIN_PACKAGE = 'logdd'
VERSION = __read_version(MAIN_PACKAGE)
DESCRIPTION = 'Extract metrics from logs and pass it to datadog statsd'
LICENCE = 'MIT License'
URL = 'https://github.com/facemetric/logdd'
AUTHOR = 'Dmitry Sorokin'
EMAIL = 'dmitry.sorokin@gmail.com'
KEYWORDS = 'datadog statsd log'

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
]

CONSOLE_SCRIPTS = [
    'logdd=logdd.cli:cli'
]


def __read(fname):
    with open(os.path.join(__location__, fname)) as f:
        return f.read()


def setup_package():
    setuptools.setup(
        name=NAME,
        version=VERSION,
        url=URL,
        description=DESCRIPTION,
        author=AUTHOR,
        author_email=EMAIL,
        license=LICENCE,
        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,
        packages=setuptools.find_packages(exclude=['test', 'tests', 'tests.*']),
        install_requires=[req for req in __read('requirements.txt').split('\\n') if req != ''],
        entry_points={
            'console_scripts': CONSOLE_SCRIPTS,
        }
    )


if __name__ == '__main__':
    setup_package()
