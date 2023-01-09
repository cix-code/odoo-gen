from setuptools import setup, find_packages
from src.constants import version as ocli_version


setup(
    name='ocli',
    version=ocli_version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==8.1.3',
    ],
    entry_points='''
        [console_scripts]
        ocli=src.ocli:cli
    ''',
)
