# To use a consistent encoding
from codecs import open as codec_open
from os import path
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

HERE_PATH = path.abspath(path.dirname(__file__))

with codec_open(path.join(HERE_PATH, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

with codec_open(path.join(HERE_PATH, 'requirements.txt'),
                encoding='utf-8') as f:
    REQUIREMENTS = [
        line for line in f.readlines()
        if line and not line.startswith('#')
    ]

with codec_open(path.join(HERE_PATH, 'requirements.dev.txt'),
                encoding='utf-8') as f:
    REQUIREMENTS_DEV = [
        line for line in f.readlines()
        if line and not line.startswith('#')
    ]

setup(
    name='apiqa-storage',
    version='2.8.1',
    description='Apiqa user storage backend for django projects',
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/pik-software/apiqa-storage.git',
    author='pik-software',
    author_email='no-reply@pik-software.ru',
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='apiqa django',

    packages=find_packages(exclude=[
        'contrib', 'docs', 'tests', 'test_project',
        'tests_storage', 'tests_storage.*',
    ]),

    # https://packaging.python.org/en/latest/requirements.html
    install_requires=REQUIREMENTS,
    python_requires='~=3.6',

    # List additional groups of dependencies here
    #   $ pip install sampleproject[dev]
    extras_require={
        'dev': REQUIREMENTS_DEV,
    },

    project_urls={
        'Bug Reports': 'https://gitlab.pik-software.ru/'
                       'apiqa/apiqa-storage/issues',
        'Funding': 'https://gitlab.pik-software.ru/apiqa/apiqa-storage',
        'Say Thanks!': 'https://saythanks.io/to/pik_software',
        'Source': 'https://gitlab.pik-software.ru/apiqa/apiqa-storage',
    },
)
