import os,sys
from setuptools import setup,find_packages

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

setup(
    name="IndianPines",
    version="0.0.1",
    install_requires=["scikit-learn", "numpy","pandas"],
    #description='Sample package for Python-Guide.org',
    #long_description=readme,
    author='Kotaro Sonoda',
    author_email='kotaro1976@gmail.com',
    #install_requires=read_requirements(),
    url='https://github.com/helmenov/IndianPines',
    #license=license,
    packages=find_packages(),
)
