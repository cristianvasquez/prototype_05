#  Copyright (c) 2021.

from setuptools import setup, find_packages

README = open('README.md', 'r').read()

setup(
    name='obsidian_graphs',
    version='0.0.1',
    packages=find_packages(),
    package_data={'': ['static/', 'templates/']},
    include_package_data=True,
    url='https://github.com/aquilesC/static_website_builder',
    license='MIT',
    author='Cristian Vasquez',
    description='Basic analysis of your Obsidian graph',
    long_description=README,
    entry_points={
        'console_scripts': [
            'brain_dump=src.main:main'
        ]
    },
    install_requires=[
        'markdown',
        'markdown-checklist',
        'pyembed-markdown',
        'python-frontmatter',
    ]
)
