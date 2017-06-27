#! /usr/bin/env python3

import setuptools

setuptools.setup(
  name='vimdecrypt',
  version='0.9',
  author='Gertjan van Zwieten',
  py_modules=['vimdecrypt'],
  entry_points={
    'console_scripts': ['vimdecrypt=vimdecrypt:cli'],
  },
)
