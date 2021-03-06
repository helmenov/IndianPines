import os,sys
from setuptools import setup,find_packages

setup(
    name="IndianPines",
    version="0.0.3",
    install_requires=["scikit-learn", "numpy","pandas"],
    description='Indian Pines datasets for scikit-learn',
    long_description=open('Readme.md',encoding='utf-8').read(),
    author='Kotaro Sonoda',
    author_email='kotaro1976@gmail.com',
    url='https://github.com/helmenov/IndianPines',
    packages=find_packages(),
    include_package_data=True,
)
