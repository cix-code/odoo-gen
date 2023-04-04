"""
oGen setuptools definition
"""

from setuptools import setup, find_packages
from src.constants import VERSION


setup(
    name='ogen',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.3',
        'configparser==5.3.0',
        'PyYAML==6.0',
    ],
    entry_points='''
        [console_scripts]
        ogen=src.ogen:gen
    ''',
)
