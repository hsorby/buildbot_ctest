
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'buildbot_ctest', 'version.txt'), encoding='utf-8') as f:
    version = f.read()

print('"%s"' % version)

setup(
    name='buildbot_ctest',
    version=version,
    description='A Buildbot build step plugin for running CTest and reporting pass rate.',
    long_description=long_description,
    url='https://github.com/hsorby/buildbot_ctest',
    keywords='buildbot buildbot-plugin',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['buildbot>=0.9.1'],
    package_data={
        'buildbot_ctest': ['version.txt'],
    },
    entry_points={
        'buildbot.steps': [
            'CTest = buildbot_ctest.ctest:CTest'
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache 2.0 License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)