__author__ = 'jingxuan'
from setuptools import setup, find_packages

setup(
  name='genomeapi',
  version='1.0',
  packages=find_packages(),
  install_requires=['pandas','requests','configparser'],
  license='Dspark Mobility Genome',
  long_description=open('README.md').read()
)
