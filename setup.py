#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

# with open('HISTORY.rst') as history_file:
#     history = history_file.read()


def required(fname):
    return filter(lambda x: not x.startswith('-'), open(fname).readlines())

requirements = [i.strip() for i in open("requirements.txt").readlines()]

setup(
    name='SlurmDBD-XdMod-migration',
    version='0.1.0',
    description="Migrate old slurm (v2.0.5) database to XdMod databases",
    long_description=readme,  # + '\n\n' + history,
    author="Domingos Rodrigues",
    author_email='ddcr@lcc.ufmg.br',
    url='https://github.com/ddcr/SlurmDBD-XdMod-migration/',
    packages=['src'],
    package_dir={'Slurmdbd-XdMod-migration': 'src'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    platforms='any',
    keywords='',
    # entry_points={
    #     'console_scripts': [
    #         'my-tool = my_tool.cli:main',
    #     ],
    # },
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='tests',
)
