from distutils.core import setup
from setuptools import find_packages

_packages = find_packages(exclude=["*test*"])

setup(
    name='jeeves',
    version='0.1',
    packages=_packages,
    install_requires=[
        'fabric',
    ],
)
