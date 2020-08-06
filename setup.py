#  Copyright © DataSpark Pte Ltd 2014 - 2020.
#
#  This software and any related documentation contain confidential and proprietary information of
#  DataSpark and its licensors (if any). Use of this software and any related documentation is
#  governed by the terms of your written agreement with DataSpark. You may not use, download or
#  install this software or any related documentation without obtaining an appropriate licence
#  agreement from DataSpark.
#
#  All rights reserved.

"""
   This is for setup

   @author: jingxuan
   @maintainer: jingxuan
   @last editor: jingxuan
   @last edit time: 3/4/20
"""

from setuptools import setup, find_packages

setup(
  name='genomeapi',
  version='1.0.8',
  packages=find_packages(),
  install_requires=['pandas>=1.0.1',
                    'requests>=2.23.0',
                    'configparser>=4.0.2'],
  license='Dspark Mobility Genome',
  long_description=open('README.md').read()
)
