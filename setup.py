"""
oCLI setuptools definition
"""

from setuptools import setup, find_packages
from src.constants import VERSION


setup(
    name='ocli',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.3',
        'configparser==5.3.0',
    ],
    entry_points='''
        [console_scripts]
        ocli=src.ocli:cli
    ''',
)
