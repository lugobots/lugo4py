import setuptools
from distutils.core import setup

setup(
  name='test',
  packages=setuptools.find_packages(),
  version='1.0.0',
  license='MIT',
  description='',
  author='',
  author_email='',
  url='https://github.com/lugobots/lugo4py',
  download_url='https://github.com/lugobots/lugo4py/archive/v1.0.0.tar.gz',
  keywords=[],
  install_requires=[
          'grpcio',
          'protobuf',
      ],
  classifiers=[
  ],
)
