"""
oGen setuptools definition
"""

from setuptools import setup, find_packages
from setuptools.config import read_configuration

setup_cfg = read_configuration("setup.cfg")
metadata = setup_cfg["metadata"]

cmd_name = metadata['name']

setup(
    name=cmd_name,
    version=metadata['version'],
    packages=find_packages(),
    include_package_data=True,
    long_description=metadata['long_description'],
    long_description_content_type='text/markdown',
    install_requires=[
        'click==8.1.3',
        'configparser==5.3.0',
        'PyYAML==6.0',
    ],
    entry_points=f'''
        [console_scripts]
        {cmd_name}=src.ogen:gen
    ''',
)
