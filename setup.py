__author__ = 'jingxuan'
from setuptools import setup, find_packages

setup(
  name='genomeapi',
  version='1.01',
  packages=find_packages(),
  install_requires=['pandas==1.0.1',
                    'requests==2.23.0',
                    'configparser==4.0.2'],
  license='Dspark Mobility Genome',
  long_description=open('README.md').read()
)
