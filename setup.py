#!/usr/bin/env python

import os
import re
from subprocess import check_output

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'Pipfile')) as pipfile:
    content = pipfile.read()
    REQUIREMENTS = re.findall(r'''\\n *['"]?([\w-]*)['"]? *=''', content.split('packages]')[1])

VERSION = [tag for tag in check_output(['git', 'tag', '-l']).decode().split() if tag.startswith('v')][-1][1:]

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='cup',
    version=VERSION,
    packages=['cup'],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    license='BSD',
    description='Nim’s Django Helpers',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/nim65s/cup',
    author='Guilhem Saurel',
    author_email='webmaster@saurel.me',
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
