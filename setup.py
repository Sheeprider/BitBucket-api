# -*- coding: utf-8 -*-
from distutils.core import setup

import bitbucket

setup(
  name='bitbucket',
  version=bitbucket.__version__,
  description='Bitbucket API',
  author='Baptiste Millou',
  author_email='baptiste@smoothie-creative.com',
  url='https://github.com/Sheeprider/Py-BitBucket',
  packages=['bitbucket'],
  license='GPL',
  install_requires=open('requirements.txt').readlines(),
  )
