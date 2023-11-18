# Copyright 2023 Enzo Venturi. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from setuptools import setup, find_packages

setup(
    name='y2d',
    version='0.0.1',
    description='Generate Anki packages from YAML files',
    author='Enzo Venturi',
    url='https://gitlab.com/nzv/y2d',
    packages=find_packages(),
    install_requires=[
        'markdown',
        'pygments',
        'genanki',
        'PyYAML',
        'python-slugify',
    ],
    entry_points={
        'console_scripts': [
            'y2d = y2d.__main__:main',
        ],
    },
)
