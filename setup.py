import os,sys
from setuptools import setup,find_packages

setup(
    name="IndianPines",
    version="0.0.2",
    install_requires=["scikit-learn", "numpy","pandas"],
    description='Indian Pines datasets for scikit-learn',
    long_description=Readme.md,
    author='Kotaro Sonoda',
    author_email='kotaro1976@gmail.com',
    url='https://github.com/helmenov/IndianPines',
    license=MIT,
    packages=find_packages(),
    include_package_data=True,
)
