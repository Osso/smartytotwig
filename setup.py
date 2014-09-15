#!/usr/bin/env python
from setuptools import setup, find_packages
import ConfigParser

# Read version.conf and use the version #.
config = ConfigParser.ConfigParser()
config.readfp(open('version.conf'))

setup(name="smartytotwig",
      version=config.get('app:main', 'version'),
      description="Converts Smarty templates into Twig templates.",
      author="Ben Coe",
      author_email="coe@freshbooks.com",
      entry_points={
          'console_scripts': [
              'smartytotwig = smartytotwig.main:main'
          ]
      },
      url="git@github.com:freshbooks/smartytotwig.git",
      packages=find_packages(),
      include_package_data=True,
      setup_requires=['setuptools-git'],
      install_requires=['simplejson==2.1.1'],
      tests_require=['nose', 'coverage'],
      )
