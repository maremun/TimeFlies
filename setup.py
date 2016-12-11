#!/usr/bin/env python3
#   setup.py

from setuptools import find_packages, setup

setup(name='timeflies',
      packages=find_packages(),
      entry_points={
          'console_scripts': [
              'timeflies = timeflies.bot:main',
          ],
      })
