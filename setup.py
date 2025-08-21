import os
import sys
from typing import List
from setuptools import setup, find_packages

setup(
    name='bhaskarmishradata',
    version='0.0.1',
    author='Bhaskar Mishra',
    author_email='bhaskarmishra1590@gmail.com',
    description='A data processing and analysis package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    python_requires='>=3.8',
)
