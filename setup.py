#!/usr/bin/env python
from setuptools import setup, find_packages


setup(name="smartytotwig",
      version='0.1',
      description="Converts Smarty templates into Twig templates.",
      author="Alessio Deiana",
      author_email="adeiana@gmail.com",
      entry_points={
          'console_scripts': [
              'smartytotwig = smartytotwig.main:main'
          ]
      },
      url="git@github.com:osso/smartytotwig.git",
      packages=find_packages(),
      include_package_data=True,
      setup_requires=['setuptools-git'],
      install_requires=['simplejson==2.1.1'],
      )
